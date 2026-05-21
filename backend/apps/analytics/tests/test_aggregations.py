"""Analytics aggregation testlari."""
import pytest
from datetime import timedelta
from django.utils import timezone

from apps.analytics import aggregations
from apps.analytics.filters import DateRange
from apps.tracking.models import PageView, Session

pytestmark = pytest.mark.django_db


def _range(days: int = 7) -> DateRange:
    end = timezone.now()
    start = end - timedelta(days=days)
    return DateRange(start=start, end=end)


def _make_session(site, **kwargs):
    return Session.objects.create(
        site=site,
        session_uid=kwargs.get("uid", "u1"),
        ip_hash="x",
        country=kwargs.get("country", "Uzbekistan"),
        country_code=kwargs.get("country_code", "UZ"),
        browser=kwargs.get("browser", "Chrome"),
        os=kwargs.get("os", "Windows"),
        device=kwargs.get("device", "Desktop"),
        is_mobile=kwargs.get("is_mobile", False),
        is_bounce=kwargs.get("is_bounce", False),
        page_count=kwargs.get("page_count", 1),
        duration_sec=kwargs.get("duration_sec", 60),
    )


class TestOverview:
    def test_empty_returns_zeros(self, site):
        result = aggregations.overview(site.id, _range())
        assert result["total_pageviews"] == 0
        assert result["total_sessions"] == 0
        assert result["bounce_rate"] == 0.0

    def test_counts_correctly(self, site):
        s1 = _make_session(site, uid="u1", is_bounce=True, page_count=1, duration_sec=10)
        s2 = _make_session(site, uid="u2", is_bounce=False, page_count=3, duration_sec=120)
        PageView.objects.create(site=site, session=s1, url="/")
        PageView.objects.create(site=site, session=s2, url="/")
        PageView.objects.create(site=site, session=s2, url="/about")
        PageView.objects.create(site=site, session=s2, url="/contact")

        result = aggregations.overview(site.id, _range())
        assert result["total_pageviews"] == 4
        assert result["total_sessions"] == 2
        assert result["unique_visitors"] == 2
        assert result["bounce_rate"] == 0.5  # 1 ta bounce / 2 sessiya


class TestTopPages:
    def test_returns_pages_sorted_by_views(self, site):
        s = _make_session(site)
        PageView.objects.bulk_create([
            PageView(site=site, session=s, url="/", title="Home"),
            PageView(site=site, session=s, url="/", title="Home"),
            PageView(site=site, session=s, url="/", title="Home"),
            PageView(site=site, session=s, url="/about", title="About"),
        ])
        results = aggregations.top_pages(site.id, _range())
        assert len(results) == 2
        assert results[0]["url"] == "/"
        assert results[0]["views"] == 3
        assert results[1]["url"] == "/about"
