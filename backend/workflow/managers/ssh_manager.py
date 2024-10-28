# import os
# from dataclasses import dataclass
# from pathlib import Path
#
# import paramiko
# from loguru import logger
#
# from functions.get_dump_command import get_dump_command
# from functions.get_paths import get_config_dump_folder_path, get_dump_filename
# from managers.config_manager import Config, ConfigManager
# from models.ssh_connection import ConfigSSHConnection
#
#
# @dataclass
# class CommandResult:
#     stdout: str
#     stderr: str
#
#     @property
#     def ok(self):
#         return not bool(self.stderr)
#
#
# class SSHManager:
#     TMP_FOLDER = '.tmp_dumps'
#
#     def __init__(self, config: Config):
#         self.config = config
#         self.ssh_connection: paramiko.SSHClient | None = None
#
#     def process(self):
#         logger.info({'event': 'SSH_START_DUMP', 'config': self.config.name})
#         self.ssh_connection = self._get_ssh_connection()
#         tmp_path = self._get_tmp_folder_path()
#         self._remove_obsolete_files(tmp_path)
#         filename = get_dump_filename()
#         file_path = str(Path(tmp_path, filename))
#         logger.info({'event': 'SSH_DUMP_INIT', 'config': self.config.name, 'file_path': file_path})
#         cmd = get_dump_command(self.config, file_path=file_path)
#         result = self._exec_command(cmd)
#         if not result.ok:
#             logger.info({'event': 'SSH_DUMP_ERROR', 'config': self.config.name, 'errors': result.stderr})
#             return
#         logger.info({'event': 'SSH_DUMP_CREATED', 'config': self.config.name, 'filename': filename})
#         file_path = self._archive_dump(file_path)
#         file_path = self._download_file(file_path)
#         self.ssh_connection.close()
#         return file_path
#
#     def _download_file(self, file_path: str):
#         filename = os.path.basename(file_path)
#         sftp = self.ssh_connection.open_sftp()
#         local_file_path = str(Path(get_config_dump_folder_path(self.config), filename))
#         sftp.get(file_path, local_file_path)
#         logger.info({'event': 'SSH_DUMP_DOWNLOADED', 'config': self.config.name, 'filename': filename})
#         sftp.close()
#         result = self._exec_command(f'rm {file_path}')
#         if result.ok:
#             logger.info({'event': 'SSH_TEMP_DUMP_REMOVED', 'config': self.config.name, 'filename': filename})
#         else:
#             logger.error({'event': 'SSH_TEMP_DUMP_REMOVE_ERROR', 'config': self.config.name, 'filename': filename})
#         return local_file_path
#
#     def _archive_dump(self, file_path: str):
#         archive_file_path = f'{file_path}.zip'
#         filename = os.path.basename(archive_file_path)
#         cmd = f'zip {archive_file_path} {file_path}'
#         self._exec_command(cmd)
#         self._exec_command(f'rm {file_path}')
#         logger.info({'event': 'SSH_DUMP_ARCHIVED', 'config': self.config.name, 'filename': filename})
#         return archive_file_path
#
#     def _get_ssh_connection(self):
#         ssh_connection = paramiko.SSHClient()
#         ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh = self.config.ssh
#         params = {'hostname': ssh.host, 'port': ssh.port, 'username': ssh.username}
#         if ssh.private_key:
#             pkey = self._get_pkey_data(ssh)
#             if not pkey:
#                 data = {'event': 'SSH_INVALID_PRIVATE_KEY', 'config': self.config.name}
#                 logger.error(data)
#                 raise ValueError(data)
#             params['pkey'] = pkey
#         else:
#             params['password'] = ssh.password
#
#         ssh_connection.connect(**params)
#         logger.info({'event': 'SSH_CONNECTED', 'config': self.config.name, 'host': ssh.host})
#         return ssh_connection
#
#     def _get_tmp_folder_path(self):
#         result = self._exec_command('pwd')
#         current_path = result.stdout.replace('\n', '')
#         tmp_folder_path = str(Path(current_path, self.TMP_FOLDER))
#         self._exec_command(f'mkdir {tmp_folder_path}')
#         return tmp_folder_path
#
#     def _remove_obsolete_files(self, tmp_path: str):
#         result = self._exec_command(f'find {tmp_path} -type f -mmin +360 -name "dump_*"')
#         files_to_delete = result.stdout.strip().splitlines()
#         deleted_count = 0
#         for file_to_delete in files_to_delete:
#             delete_result = self._exec_command(f'rm {file_to_delete}')
#             if delete_result.ok:
#                 deleted_count += 1
#         if deleted_count:
#             logger.info({'event': 'SSH_REMOVED_OBSOLETE_FILES', 'config': self.config.name, 'count': deleted_count})
#
#     def _exec_command(self, cmd: str):
#         _, stdout, stderr = self.ssh_connection.exec_command(cmd)
#         return CommandResult(
#             stdout=stdout.read().decode(),
#             stderr=stderr.read().decode(),
#         )
#
#     @staticmethod
#     def _get_pkey_data(ssh_config: ConfigSSHConnection):
#         private_key_path = str(Path(ConfigManager.get_ssh_keys_folder_path(), ssh_config.private_key))
#         _check_keys = [paramiko.RSAKey, paramiko.Ed25519Key, paramiko.DSSKey, paramiko.ECDSAKey]
#         for el in _check_keys:
#             try:
#                 return el.from_private_key_file(private_key_path, password=ssh_config.passphrase)
#             except paramiko.SSHException:
#                 pass
#         return None
