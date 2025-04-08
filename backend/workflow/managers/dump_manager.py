import glob
import os
import subprocess
import zipfile
from pathlib import Path

from workflow.functions.get_dump_command import get_dump_command
from workflow.functions.get_file_size import get_file_size, get_file_size_label_by_path
from workflow.functions.get_paths import get_config_dump_folder_path, get_dump_filename
from workflow.functions.remove_local_file import remove_local_file
from workflow.managers.dump_exception import DumpException
from workflow.managers.s3_manager import S3Manager
from workflow.managers.ssh_manager import SSHManager
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow


class DumpManager:
    def __init__(self, workflow: Workflow):
        self.config = workflow.config
        self.workflow: Workflow = workflow
        self._e: WorkflowEventManager | None = None

    def process(self):
        self._e = WorkflowEventManager(self.workflow)
        try:
            self._process()
        except DumpException as e:
            self._e.add_event(name=e.name, text=e.text, is_error=True)
            self._e.set_status(Workflow.Status.FAILED)
        except Exception as e:
            self._e.add_event(name='DUMP_UNHANDLED_ERROR', text=str(e), is_error=True)
            self._e.set_status(Workflow.Status.FAILED)

    def _process(self):
        self._e.set_status(status=Workflow.Status.IN_PROGRESS)
        file_path = self._create_dump()
        self.workflow.size = get_file_size(file_path)
        self.workflow.save(update_fields=('size',))
        if self.config.s3_connection:
            S3Manager(self.workflow).process(file_path)
        self._remove_old_files()
        self._e.set_status(status=Workflow.Status.DONE)
        self.workflow.filename = file_path.name
        self.workflow.active = True
        self.workflow.save(update_fields=('filename', 'active'))

    def _create_dump(self):
        if self.config.ssh_connection:
            file_path = SSHManager(self.workflow).process()
        else:
            dump_folder_path = get_config_dump_folder_path(self.config)
            file_path = dump_folder_path / get_dump_filename(self.config)
            cmd = get_dump_command(self.config, file_path)
            self._e.add_event('DUMP_STARTED')
            subprocess.run(cmd, shell=True, check=True)
            self._e.add_event(
                'DUMP_CREATED', f'Filename: "{file_path.name}" size: {get_file_size_label_by_path(file_path)}'
            )

            file_path = self._archive_dump(file_path)
        return file_path

    def _archive_dump(self, file_path: Path):
        self._e.add_event('ARCHIVE_DUMP_STARTED')
        archive_file_path = Path(f'{file_path}.zip')
        # filename = os.path.basename(archive_file_path)
        filename = archive_file_path.name
        with zipfile.ZipFile(archive_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
            zip_f.write(file_path, os.path.basename(file_path))
        self._e.add_event(
            'DUMP_ARCHIVED', text=f'Filename: "{filename}" size: {get_file_size_label_by_path(archive_file_path)}'
        )
        remove_local_file(file_path)
        self._e.add_event('UNARCHIVED_DUMP_REMOVED', text=f'Filename: "{file_path.name}"')
        return archive_file_path

    def _remove_old_files(self):
        dump_folder_path = get_config_dump_folder_path(self.config)
        files = glob.glob(os.path.join(dump_folder_path, '*'))
        files.sort(key=os.path.getmtime)
        if len(files) <= self.config.max_versions:
            return
        max_versions: int = self.config.max_versions
        files_to_remove = files[:-max_versions]
        deleted_count = 0
        for file in files_to_remove:
            filename = Path(file).name
            Workflow.objects.filter(config=self.config, filename=filename, active=True).update(active=False)
            if remove_local_file(file):
                deleted_count += 1
        if deleted_count:
            self._e.add_event('REMOVED_OLD_LOCAL_DUMPS', text=f'Count: {deleted_count}')
