from django.urls import include, path

from core.utils.base_urls import urlpatterns

urlpatterns += [
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('config.urls')),
    path('api/v1/', include('workflow.urls')),
]
