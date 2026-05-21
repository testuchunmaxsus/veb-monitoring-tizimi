"""Tracking biznes mantiq."""
from __future__ import annotations

import hashlib
from datetime import timedelta
from typing import Optional

from django.utils import timezone

from apps.sites.models import Site
from core.geoip import lookup as geo_lookup
from core.ua_parser import parse_ua

from .models import Event, PageView, Session


BOUNCE_THRESHOLD_SEC = 30


def hash_ip(ip: str) -> str:
    """IP manzilini SHA-256 hash qiladi (privacy)."""
    return hashlib.sha256((ip or "0.0.0.0").encode()).hexdigest()


def get_client_ip(request) -> str:
    """Request'dan haqiqiy IP olish (proxy'lar orqali)."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def find_site(api_key: str) -> Optional[Site]:
    """API kalit asosida sayt topadi."""
    return Site.objects.filter(api_key=api_key, is_active=True).first()


def get_or_create_session(*, site: Site, session_uid: str, ip: str, ua_string: str, referrer: str) -> Session:
    """Brauzer sessiyasini topadi yoki yaratadi.

    Bitta session_uid 30 daqiqa ichida bitta sessiya hisoblanadi (sliding window).
    """
    cutoff = timezone.now() - timedelta(minutes=30)
    session = (
        Session.objects.filter(site=site, session_uid=session_uid, started_at__gte=cutoff)
        .order_by("-started_at")
        .first()
    )
    if session:
        return session

    ua_data = parse_ua(ua_string)
    geo = geo_lookup(ip) or {}

    return Session.objects.create(
        site=site,
        session_uid=session_uid,
        ip_hash=hash_ip(ip),
        country=geo.get("country_name", "") or "",
        country_code=geo.get("country", "") or "",
        city=geo.get("city", "") or "",
        latitude=geo.get("latitude"),
        longitude=geo.get("longitude"),
        browser=ua_data["browser"],
        browser_version=ua_data["browser_version"],
        os=ua_data["os"],
        os_version=ua_data["os_version"],
        device=ua_data["device"],
        is_mobile=ua_data["is_mobile"],
        is_bot=ua_data["is_bot"],
        referrer=(referrer or "")[:500],
        page_count=0,
    )


def record_pageview(*, site: Site, session: Session, data: dict) -> PageView:
    """Sahifa ko'rishini yozadi va sessiya counter'ini yangilaydi."""
    pv = PageView.objects.create(
        site=site,
        session=session,
        url=data["url"][:2000],
        title=(data.get("title") or "")[:500],
        referrer=(data.get("referrer") or "")[:500],
        load_time_ms=data.get("load_time_ms"),
        lcp_ms=data.get("lcp_ms"),
        fcp_ms=data.get("fcp_ms"),
        ttfb_ms=data.get("ttfb_ms"),
    )

    Session.objects.filter(pk=session.pk).update(page_count=session.page_count + 1)
    return pv


def record_event(*, site: Site, session: Session, data: dict) -> Event:
    """Custom hodisa yozadi."""
    return Event.objects.create(
        site=site,
        session=session,
        type=data["type"],
        target=(data.get("target") or "")[:500],
        metadata=data.get("metadata") or {},
    )


def end_session(*, session: Session, duration_sec: int) -> Session:
    """Sessiya tugashini qayd etadi va bounce flag'ni hisoblaydi."""
    session.refresh_from_db()
    session.ended_at = timezone.now()
    session.duration_sec = max(duration_sec, 0)
    session.is_bounce = session.page_count <= 1 and session.duration_sec < BOUNCE_THRESHOLD_SEC
    session.save(update_fields=["ended_at", "duration_sec", "is_bounce"])
    return session
