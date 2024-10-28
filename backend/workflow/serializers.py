from air_drf_relation.serializers import AirModelSerializer

from config.serializers import ConfigSimpleSerializer

from .models import Workflow, WorkflowEvent


class WorkflowSerializer(AirModelSerializer):
    config = ConfigSimpleSerializer()

    class Meta:
        model = Workflow
        fields = ('id', 'filename', 'active', 'storage', 'config', 'status', 'created_at', 'created_by')


class WorkflowEventSerializer(AirModelSerializer):
    class Meta:
        model = WorkflowEvent
        fields = ('id', 'workflow', 'is_error', 'name', 'text', 'created_at')
