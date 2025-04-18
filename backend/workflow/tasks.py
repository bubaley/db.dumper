from celery import shared_task
from django.core.management import call_command

from config.models import Config
from core.celery.celery_enums import CeleryTasks
from core.utils.logger import Logg
from workflow.managers.dump_manager import DumpManager
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow


@shared_task(name=CeleryTasks.WORKFLOW_INIT)
def workflow_init(**kwargs):
    config_key = kwargs.get('config_key')
    workflow_id = kwargs.get('workflow_id', None)
    config = Config.objects.filter(key=config_key).first()
    if not config:
        return
    if workflow_id:
        workflow = Workflow.objects.filter(id=workflow_id).first()
        if not workflow:
            return
    else:
        workflow = WorkflowEventManager.build_workflow(config)
    DumpManager(workflow).process()


@shared_task(name=CeleryTasks.CONFIG_BUILD_WORKFLOWS)
def config_build_workflows(**kwargs):
    call_command('build_workflows')
