import os

from django.core.asgi import get_asgi_application

from core.settings import common

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')

application = get_asgi_application()