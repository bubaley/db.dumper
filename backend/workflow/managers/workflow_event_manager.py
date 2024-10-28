from loguru import logger

from config.models import Config
from user.models import User
from workflow.models import Workflow, WorkflowEvent


class WorkflowEventManager:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow

    def add_event(self, name: str, text: str | None = None, is_error=False):
        level = 'ERROR' if is_error else 'INFO'
        name = name.upper()
        logger.log(level, {'event': name, 'config': self.workflow.config.key, 'text': text})
        return WorkflowEvent.objects.create(
            workflow=self.workflow,
            name=name,
            text=text or None,
            is_error=is_error,
        )

    def set_status(self, status: Workflow.Status):
        self.workflow.status = status
        self.workflow.save(update_fields=('status',))
        events = {
            Workflow.Status.CREATED: 'WORKFLOW_CREATED',
            Workflow.Status.IN_PROGRESS: 'WORKFLOW_STARTED',
            Workflow.Status.FAILED: 'WORKFLOW_FAILED',
            Workflow.Status.DONE: 'WORKFLOW_DONE',
        }
        self.add_event(events.get(status) or 'WORKFLOW_GOT_UNHANDLED_STATUS')

    @staticmethod
    def build_workflow(config: Config, user: User = None):
        return Workflow.objects.create(
            config=config,
            created_by=user,
            storage=Workflow.Storage.LOCAL if not config.s3_connection_id else Workflow.Storage.S3,
        )
