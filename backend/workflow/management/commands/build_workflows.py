from django.core.management import BaseCommand
from workflow.tasks import workflow_init
from config.models import Config
from core.utils.logger import Logg
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_configs = Workflow.objects.filter(status__in=Workflow.ACTIVE_STATUSES).values_list('config', flat=True)
        configs = Config.objects.filter(auto_build=True).exclude(id__in=active_configs)
        Logg.info(e='config.build', msg=f'Got {len(configs)} configs')
        for config in configs:
            workflow = WorkflowEventManager.build_workflow(
                config=config,
                user=None,
            )
            workflow_init.delay(config_key=config.key, workflow_id=workflow.id)