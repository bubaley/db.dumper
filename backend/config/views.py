from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow
from workflow.serializers import WorkflowSerializer
from workflow.tasks import workflow_init

from .models import Config, DatabaseConnection, S3Connection, SSHConnection
from .serializers import ConfigSerializer, DatabaseConnectionSerializer, S3ConnectionSerializer, SSHConnectionSerializer


class SSHConnectionViewSet(viewsets.ModelViewSet):
    queryset = SSHConnection.objects.all()
    serializer_class = SSHConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class S3ConnectionViewSet(viewsets.ModelViewSet):
    queryset = S3Connection.objects.all()
    serializer_class = S3ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True)
    def build(self, request, **kwargs):
        instance = self.get_object()
        workflows = Workflow.objects.filter(status__in=Workflow.ACTIVE_STATUSES)
        if workflows.filter(config=instance).exists():
            raise ValidationError({'workflow': ['Already in progress.']})
        workflow = WorkflowEventManager.build_workflow(
            config=instance,
            user=request.user if request.user.is_authenticated else None,
        )
        data = WorkflowSerializer(workflow).data
        workflow_init.delay(config_key=instance.key, workflow_id=workflow.id)
        return Response(data)
