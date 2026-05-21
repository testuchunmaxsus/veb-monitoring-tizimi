"""Tracking endpointlari (public)."""
from django.urls import path

from .views import EventIngestView, PageViewIngestView, SessionEndView

app_name = "tracking"

urlpatterns = [
    path("pageview/", PageViewIngestView.as_view(), name="pageview"),
    path("event/", EventIngestView.as_view(), name="event"),
    path("session/end/", SessionEndView.as_view(), name="session-end"),
]
