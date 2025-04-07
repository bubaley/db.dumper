from core.utils.router import BaseSimpleRouter

from .views import ConfigViewSet, DatabaseConnectionViewSet, S3ConnectionViewSet, SSHConnectionViewSet

router = BaseSimpleRouter()
router.register('ssh_connections', SSHConnectionViewSet)
router.register('s3_connections', S3ConnectionViewSet)
router.register('database_connections', DatabaseConnectionViewSet)
router.register('configs', ConfigViewSet)
urlpatterns = router.urls
