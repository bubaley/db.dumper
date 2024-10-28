from core.utils.base_simple_router import BaseSimpleRouter

from .views import WorkflowEventViewSet, WorkflowViewSet

router = BaseSimpleRouter()
router.register('workflows', WorkflowViewSet)
router.register('workflow_events', WorkflowEventViewSet)
urlpatterns = router.urls
