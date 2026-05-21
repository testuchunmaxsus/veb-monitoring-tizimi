"""Tracking endpointlari testlari."""
import pytest
from rest_framework import status

from apps.tracking.models import Event, PageView, Session

pytestmark = pytest.mark.django_db


class TestPageViewIngest:
    URL = "/api/v1/track/pageview/"

    def test_creates_pageview_with_valid_api_key(self, api_client, site):
        resp = api_client.post(self.URL, {
            "api_key": site.api_key,
            "session_uid": "test-uid-1",
            "url": "https://test.com/page",
            "title": "Page",
            "load_time_ms": 1200,
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert PageView.objects.count() == 1
        pv = PageView.objects.first()
        assert pv.site == site
        assert pv.url == "https://test.com/page"
        assert pv.session.session_uid == "test-uid-1"

    def test_rejects_invalid_api_key(self, api_client):
        resp = api_client.post(self.URL, {
            "api_key": "vmt_invalid",
            "session_uid": "x",
            "url": "https://x.com",
        }, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert PageView.objects.count() == 0

    def test_reuses_session_within_30min(self, api_client, site):
        for _ in range(2):
            resp = api_client.post(self.URL, {
                "api_key": site.api_key,
                "session_uid": "same-uid",
                "url": "https://test.com/",
            }, format="json")
            assert resp.status_code == status.HTTP_201_CREATED
        # Faqat bitta sessiya yaratilgan
        assert Session.objects.count() == 1
        assert PageView.objects.count() == 2


class TestEventIngest:
    URL = "/api/v1/track/event/"

    def test_creates_click_event(self, api_client, site):
        resp = api_client.post(self.URL, {
            "api_key": site.api_key,
            "session_uid": "uid",
            "type": "click",
            "target": "button.cta",
            "metadata": {"x": 100, "y": 200},
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
        e = Event.objects.first()
        assert e.type == "click"
        assert e.metadata == {"x": 100, "y": 200}

    def test_rejects_invalid_event_type(self, api_client, site):
        resp = api_client.post(self.URL, {
            "api_key": site.api_key,
            "session_uid": "uid",
            "type": "INVALID",
            "target": "x",
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
