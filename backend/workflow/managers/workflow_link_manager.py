import os

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from workflow.functions.get_paths import get_config_dump_folder_path
from workflow.managers.s3_manager import S3Manager
from workflow.models import Workflow


class WorkflowLinkManager:
    def __init__(self, workflow: Workflow, request: Request):
        self.workflow = workflow
        self.request: Request = request

    def process(self):
        if not self.workflow.active:
            raise ValidationError({'workflow': ['Inactive.']})
        config = self.workflow.config
        if self.workflow.storage == Workflow.Storage.LOCAL:
            file_path = get_config_dump_folder_path(config) / self.workflow.filename
            if not os.path.exists(file_path):
                self._raise_invalid_file()
            return {
                'url': self.request.build_absolute_uri(f'/dumps/{config.key}/{self.workflow.filename}'),
                'filename': self.workflow.filename,
            }
        elif self.workflow.storage == Workflow.Storage.S3:
            url = S3Manager(self.workflow).get_file_url()
            if not url:
                self._raise_invalid_file()
            return {
                'url': url,
                'filename': self.workflow.filename,
            }

    def _raise_invalid_file(self):
        self.workflow.active = False
        self.workflow.save(update_fields=('active',))
        raise ValidationError({'workflow': ['File already removed.']})
