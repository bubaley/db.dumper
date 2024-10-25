import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from models.config_settings import ConfigSettings
from models.database_connection import ConfigDatabaseConnection
from models.s3_connection import ConfigS3Connection, S3Connection
from models.ssh_connection import ConfigSSHConnection, SSHConnection


class Config(BaseModel):
    settings: ConfigSettings
    database: ConfigDatabaseConnection
    s3: ConfigS3Connection | None = None
    ssh: ConfigSSHConnection | None = None

    @property
    def name(self):
        return self.settings.name


class Specification(BaseModel):
    ssh: list[SSHConnection] = []
    s3: list[S3Connection] = []
    configs: list[Config] = []


class ConfigManager:
    _instance = None

    def __init__(self):
        self._check_dumps_folder()
        if not hasattr(self, 'initialized'):
            self.specification: Specification = self._prepare_specification()
            self.configs: list[Config] = self._fill_configs()
            self._config_by_names = {v.name: v for v in self.configs}
            self.initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _prepare_specification():
        config_path = Path(Path(__file__).parent.parent, 'config.yaml')
        with open(config_path) as file:
            yaml_result = yaml.safe_load(file) or {}
            try:
                return Specification(**yaml_result)
            except ValidationError as e:
                _data = {'event': 'PARSE_CONFIG_ERROR', 'errors': e.errors()}
                raise ValueError(_data)

    def _fill_configs(self):
        errors = []
        ssh_by_names = {v.name: v for v in self.specification.ssh}
        s3_by_names = {v.name: v for v in self.specification.s3}
        configs: list[Config] = []
        ssh_keys_path = self.get_ssh_keys_folder_path()
        for el in self.specification.configs:
            if el.s3:
                el.settings.s3_name = None
            elif el.settings.s3_name:
                el.s3 = s3_by_names.get(el.settings.s3_name)
                if not el.s3:
                    errors.append(f'Config "{el.name}" has invalid s3_name "{el.settings.s3_name}"')
            if el.ssh:
                el.settings.ssh_name = None
            elif el.settings.ssh_name:
                el.ssh = ssh_by_names.get(el.settings.ssh_name)
                if not el.ssh:
                    errors.append(f'Config "{el.name}" has invalid ssh_name "{el.settings.ssh_name}"')
            if el.ssh and el.ssh.private_key:
                if not os.path.exists(Path(ssh_keys_path, el.ssh.private_key)):
                    errors.append(f'Config "{el.name}" has invalid ssh private_key "{el.ssh.private_key}"')
            configs.append(el)
        if errors:
            _text = 'Invalid configs\n' + '\n'.join(errors)
            raise ValueError(_text)
        return configs

    def get_config_by_name(self, name: str):
        return self._config_by_names.get(name) or None

    @staticmethod
    def get_ssh_keys_folder_path():
        return str(Path(Path(__file__).parent.parent, 'ssh_keys'))

    @staticmethod
    def get_dumps_folder_path():
        return str(Path(Path(__file__).parent.parent, 'dumps'))

    @staticmethod
    def _check_dumps_folder():
        _path = ConfigManager.get_dumps_folder_path()
        if not os.path.exists(_path):
            raise ValueError('"dumps" folder is missing.')
