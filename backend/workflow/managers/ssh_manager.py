import io
import os
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import paramiko
from loguru import logger

from config.models import SSHConnection
from workflow.functions.get_dump_command import get_dump_command
from workflow.functions.get_paths import get_config_dump_folder_path, get_dump_filename
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow


@dataclass
class CommandResult:
    stdout: str
    stderr: str

    @property
    def ok(self):
        return not bool(self.stderr)


class SSHManager:
    TMP_FOLDER = '.tmp_dumps'

    def __init__(self, workflow: Workflow):
        self.ssh_connection: paramiko.SSHClient | None = None
        self.config = workflow.config
        self.workflow: Workflow = workflow
        self._e: WorkflowEventManager | None = None

    def process(self):
        self._e = WorkflowEventManager(self.workflow)
        self._e.add_event(name='SSH_UPLOAD_PREPARED')
        self.ssh_connection = self._get_ssh_connection()
        tmp_path = self._get_tmp_folder_path()
        self._remove_obsolete_files(tmp_path)
        filename = get_dump_filename(self.config)
        file_path = str(Path(tmp_path, filename))
        self._e.add_event(name='SSH_DUMP_INIT', text=f'file_path: {file_path}')
        cmd = get_dump_command(self.config, file_path=file_path)
        result = self._exec_command(cmd)
        if not result.ok:
            self._e.add_event(name='SSH_DUMP_ERROR', text=f'errors: {result.stderr}', is_error=True)
            logger.info({'event': 'SSH_DUMP_ERROR', 'config': self.config.name, 'errors': result.stderr})
            return
        self._e.add_event(name='SSH_DUMP_CREATED', text=f'filename: {filename}')
        file_path = self._archive_dump(file_path)
        file_path = self._download_file(file_path)
        self.ssh_connection.close()
        return file_path

    def _download_file(self, file_path: str):
        filename = os.path.basename(file_path)
        sftp = self.ssh_connection.open_sftp()
        local_file_path = Path(get_config_dump_folder_path(self.config), filename)
        sftp.get(file_path, str(local_file_path))
        self._e.add_event(name='SSH_DUMP_DOWNLOADED', text=f'filename: {filename}')
        sftp.close()
        result = self._exec_command(f'rm {file_path}')
        if result.ok:
            self._e.add_event(name='SSH_TEMP_DUMP_REMOVED', text=f'filename: {filename}')
        else:
            self._e.add_event(name='SSH_TEMP_DUMP_REMOVE_ERROR', text=f'filename: {filename}', is_error=True)
        return local_file_path

    def _archive_dump(self, file_path: str):
        archive_file_path = f'{file_path}.zip'
        filename = os.path.basename(archive_file_path)
        cmd = f'zip -j {archive_file_path} {file_path}'
        self._exec_command(cmd)
        self._exec_command(f'rm {file_path}')
        self._e.add_event(name='SSH_DUMP_ARCHIVED', text=f'filename: {filename}')
        return archive_file_path

    def _get_ssh_connection(self):
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh = self.config.ssh_connection
        params = {'hostname': ssh.host, 'port': ssh.port, 'username': ssh.username}
        if ssh.type == SSHConnection.Type.PRIVATE_KEY:
            pkey = self._get_pkey_data(ssh)
            if not pkey:
                self._e.add_event(name='SSH_INVALID_PRIVATE_KEY', is_error=True)
            params['pkey'] = pkey
        else:
            params['password'] = ssh.password
        ssh_connection.connect(**params)
        self._e.add_event(name='SSH_CONNECTED')
        return ssh_connection

    def _get_tmp_folder_path(self):
        result = self._exec_command('pwd')
        current_path = result.stdout.replace('\n', '')
        tmp_folder_path = str(Path(current_path, self.TMP_FOLDER))
        self._exec_command(f'mkdir {tmp_folder_path}')
        return tmp_folder_path

    def _remove_obsolete_files(self, tmp_path: str):
        result = self._exec_command(f'find {tmp_path} -type f -mmin +360 -name "dump_*"')
        files_to_delete = result.stdout.strip().splitlines()
        deleted_count = 0
        for file_to_delete in files_to_delete:
            delete_result = self._exec_command(f'rm {file_to_delete}')
            if delete_result.ok:
                deleted_count += 1
        if deleted_count:
            self._e.add_event(name='SSH_REMOVED_OBSOLETE_FILES', text=f'deleted: {deleted_count}')

    def _exec_command(self, cmd: str):
        _, stdout, stderr = self.ssh_connection.exec_command(cmd)
        return CommandResult(
            stdout=stdout.read().decode(),
            stderr=stderr.read().decode(),
        )

    @staticmethod
    def _get_pkey_data(ssh_config: SSHConnection):
        _check_keys = [paramiko.RSAKey, paramiko.Ed25519Key, paramiko.DSSKey, paramiko.ECDSAKey]
        for el in _check_keys:
            key_file = io.StringIO(ssh_config.private_key.strip())
            try:
                _password = (
                    ssh_config.passphrase if ssh_config.type == SSHConnection.Type.PRIVATE_KEY_WITH_PASSPHRASE else None
                )
                return el.from_private_key(key_file, password=_password)
            except Exception:
                continue
        return None
