from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .managers.workflow_link_manager import WorkflowLinkManager
from .models import Workflow, WorkflowEvent
from .serializers import WorkflowEventSerializer, WorkflowSerializer


class WorkflowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    filterset_fields = ('config',)
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['GET'], detail=True)
    def url(self, request, **kwargs):
        instance = self.get_object()
        result = WorkflowLinkManager(workflow=instance, request=request).process()
        return Response(result)


class WorkflowEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkflowEvent.objects.all()
    serializer_class = WorkflowEventSerializer
    filterset_fields = ('workflow',)
    # permission_classes = [permissions.IsAuthenticated]
