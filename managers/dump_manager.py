import glob
import os
import subprocess
import zipfile
from pathlib import Path

from loguru import logger

from functions.get_dump_command import get_dump_command
from functions.get_paths import get_config_dump_folder_path, get_dump_filename
from functions.remove_local_file import remove_local_file
from managers.config_manager import Config
from managers.s3_manager import S3Manager
from managers.ssh_manager import SSHManager


class DumpManager:
    def __init__(self, config: Config):
        self.config = config

    def process(self):
        logger.info({'event': 'START_DUMP', 'config': self.config.name})
        file_path = self._create_dump()
        if self.config.s3:
            S3Manager(self.config).process(file_path)
        self._remove_old_files()

    def _create_dump(self):
        if self.config.ssh:
            file_path = SSHManager(self.config).process()
        else:
            dump_folder_path = get_config_dump_folder_path(self.config)
            filename = get_dump_filename()
            file_path = str(Path(dump_folder_path, filename))
            logger.info({'event': 'DUMP_INIT', 'config': self.config.name, 'file_path': file_path})
            cmd = get_dump_command(self.config, file_path)
            subprocess.run(cmd, shell=True, check=True)
            logger.info({'event': 'DUMP_CREATED', 'config': self.config.name, 'filename': filename})
            file_path = self._archive_dump(file_path)
        return file_path

    def _archive_dump(self, file_path: str):
        archive_file_path = f'{file_path}.zip'
        filename = os.path.basename(archive_file_path)
        with zipfile.ZipFile(archive_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
            zip_f.write(file_path, os.path.basename(file_path))
        remove_local_file(file_path)
        logger.info({'event': 'DUMP_ARCHIVED', 'config': self.config.name, 'filename': filename})
        return archive_file_path

    def _remove_old_files(self):
        dump_folder_path = get_config_dump_folder_path(self.config)
        files = glob.glob(os.path.join(dump_folder_path, '*'))
        files.sort(key=os.path.getmtime)
        if len(files) <= self.config.settings.max_versions:
            return
        files_to_remove = files[: -self.config.settings.max_versions]
        deleted_count = 0
        for file in files_to_remove:
            if remove_local_file(file):
                deleted_count += 1
        if deleted_count:
            logger.info({'event': 'REMOVED_OLD_FILES', 'config': self.config.name, 'count': deleted_count})
