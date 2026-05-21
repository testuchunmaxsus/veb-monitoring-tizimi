"""Analytics endpointlari."""
from django.urls import path

from .views import (
    DevicesView,
    EventsBreakdownView,
    GeoView,
    OverviewView,
    TimeseriesView,
    TopPagesView,
    TopReferrersView,
)

app_name = "analytics"

urlpatterns = [
    path("overview/", OverviewView.as_view(), name="overview"),
    path("timeseries/", TimeseriesView.as_view(), name="timeseries"),
    path("top-pages/", TopPagesView.as_view(), name="top-pages"),
    path("top-referrers/", TopReferrersView.as_view(), name="top-referrers"),
    path("devices/", DevicesView.as_view(), name="devices"),
    path("geo/", GeoView.as_view(), name="geo"),
    path("events/", EventsBreakdownView.as_view(), name="events"),
]
