"""WebSocket URL routing."""
from django.urls import re_path

from .consumers import SiteConsumer

websocket_urlpatterns = [
    re_path(r"^ws/site/(?P<site_id>\d+)/$", SiteConsumer.as_asgi()),
]
