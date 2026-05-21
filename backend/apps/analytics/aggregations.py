"""Analytics aggregation queries."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from django.db.models import Avg, Count, F, Q
from django.db.models.functions import Coalesce, TruncDate, TruncHour

from apps.tracking.models import Event, PageView, Session

from .filters import DateRange


def overview(site_id: int, rng: DateRange) -> dict[str, Any]:
    """Umumiy ko'rsatkichlar."""
    pv_qs = PageView.objects.filter(site_id=site_id, timestamp__gte=rng.start, timestamp__lte=rng.end)
    sess_qs = Session.objects.filter(site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end)

    total_pageviews = pv_qs.count()
    total_sessions = sess_qs.count()
    unique_visitors = sess_qs.values("session_uid").distinct().count()
    bounce_count = sess_qs.filter(is_bounce=True).count()
    bounce_rate = round(bounce_count / total_sessions, 3) if total_sessions else 0.0
    avg_duration = sess_qs.aggregate(v=Coalesce(Avg("duration_sec"), 0.0))["v"]

    return {
        "total_pageviews": total_pageviews,
        "unique_visitors": unique_visitors,
        "total_sessions": total_sessions,
        "bounce_rate": bounce_rate,
        "avg_session_duration_sec": round(float(avg_duration or 0)),
    }


def timeseries(site_id: int, rng: DateRange, *, interval: str = "day", metric: str = "pageviews") -> list[dict]:
    """Vaqt bo'yicha grafik ma'lumotlari."""
    trunc = TruncDate("timestamp") if interval == "day" else TruncHour("timestamp")
    sess_trunc = TruncDate("started_at") if interval == "day" else TruncHour("started_at")

    if metric == "pageviews":
        qs = (
            PageView.objects.filter(site_id=site_id, timestamp__gte=rng.start, timestamp__lte=rng.end)
            .annotate(bucket=trunc)
            .values("bucket")
            .annotate(value=Count("id"))
            .order_by("bucket")
        )
    elif metric == "sessions":
        qs = (
            Session.objects.filter(site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end)
            .annotate(bucket=sess_trunc)
            .values("bucket")
            .annotate(value=Count("id"))
            .order_by("bucket")
        )
    elif metric == "visitors":
        qs = (
            Session.objects.filter(site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end)
            .annotate(bucket=sess_trunc)
            .values("bucket")
            .annotate(value=Count("session_uid", distinct=True))
            .order_by("bucket")
        )
    else:
        return []

    return [
        {"timestamp": _to_iso(row["bucket"]), "value": row["value"]}
        for row in qs
    ]


def top_pages(site_id: int, rng: DateRange, *, limit: int = 10) -> list[dict]:
    qs = (
        PageView.objects.filter(site_id=site_id, timestamp__gte=rng.start, timestamp__lte=rng.end)
        .values("url")
        .annotate(
            views=Count("id"),
            unique_visitors=Count("session__session_uid", distinct=True),
            title=F("title"),
        )
        .order_by("-views")[:limit]
    )
    return [
        {"url": r["url"], "title": r["title"] or "", "views": r["views"], "unique_visitors": r["unique_visitors"]}
        for r in qs
    ]


def top_referrers(site_id: int, rng: DateRange, *, limit: int = 10) -> list[dict]:
    qs = (
        Session.objects.filter(site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end)
        .values("referrer")
        .annotate(visits=Count("id"))
        .order_by("-visits")[:limit]
    )
    results = []
    for r in qs:
        ref = r["referrer"] or "direct"
        # domain ekstrakt (sodda, schema o'chirilgan)
        if ref != "direct" and "://" in ref:
            ref = ref.split("://", 1)[1].split("/", 1)[0]
        results.append({"referrer": ref or "direct", "visits": r["visits"]})
    return results


def devices(site_id: int, rng: DateRange) -> dict[str, list[dict]]:
    sess_qs = Session.objects.filter(site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end)

    by_device = list(
        sess_qs.values(name=F("device"))
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )
    by_browser = list(
        sess_qs.values(name=F("browser"))
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )
    by_os = list(
        sess_qs.values(name=F("os"))
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    by_type = sess_qs.aggregate(
        mobile=Count("id", filter=Q(is_mobile=True)),
        desktop=Count("id", filter=Q(is_mobile=False)),
    )

    return {
        "by_type": [
            {"name": "Mobile", "count": by_type["mobile"] or 0},
            {"name": "Desktop", "count": by_type["desktop"] or 0},
        ],
        "by_browser": _normalize(by_browser),
        "by_os": _normalize(by_os),
        "by_device": _normalize(by_device),
    }


def geo(site_id: int, rng: DateRange, *, limit: int = 20) -> dict[str, list[dict]]:
    sess_qs = Session.objects.filter(
        site_id=site_id, started_at__gte=rng.start, started_at__lte=rng.end,
    )
    by_country = list(
        sess_qs.exclude(country_code="").values("country_code", "country")
        .annotate(visits=Count("id"))
        .order_by("-visits")[:limit]
    )
    by_city = list(
        sess_qs.exclude(city="").values("city", "country_code")
        .annotate(visits=Count("id"))
        .order_by("-visits")[:limit]
    )
    return {
        "by_country": [
            {"code": r["country_code"], "name": r["country"] or r["country_code"], "visits": r["visits"]}
            for r in by_country
        ],
        "by_city": [
            {"name": r["city"], "country": r["country_code"], "visits": r["visits"]}
            for r in by_city
        ],
    }


def event_breakdown(site_id: int, rng: DateRange) -> list[dict]:
    qs = (
        Event.objects.filter(site_id=site_id, timestamp__gte=rng.start, timestamp__lte=rng.end)
        .values("type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return [{"type": r["type"], "count": r["count"]} for r in qs]


def _normalize(rows: list[dict]) -> list[dict]:
    return [{"name": r["name"] or "Unknown", "count": r["count"]} for r in rows]


def _to_iso(value) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value) + "T00:00:00"
