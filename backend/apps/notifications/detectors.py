"""Anomaliya detektori — trafik ozayishi/oshib ketishini aniqlaydi."""
from __future__ import annotations

import logging
from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone

from apps.sites.models import Site
from apps.tracking.models import PageView

from .models import Notification

logger = logging.getLogger(__name__)

# Threshold: o'tgan 7 kun shu soatdagi o'rtacha bilan solishtirib ±50% chetlanish
THRESHOLD_PCT = 50
LOOKBACK_DAYS = 7
WINDOW_MINUTES = 60
DEDUP_WINDOW_MINUTES = 60  # Bir saytga bir soatda 1 ta anomaliya bildirishnoma


def detect_for_site(site: Site) -> Notification | None:
    """Bitta sayt uchun anomaliya tekshiradi va kerak bo'lsa bildirishnoma yaratadi."""
    now = timezone.now()
    window_start = now - timedelta(minutes=WINDOW_MINUTES)

    # Hozirgi soat trafigi
    current = PageView.objects.filter(
        site=site, timestamp__gte=window_start, timestamp__lte=now,
    ).count()

    # O'tgan 7 kun shu soatda o'rtacha
    lookback_start = now - timedelta(days=LOOKBACK_DAYS)
    historical = (
        PageView.objects.filter(
            site=site,
            timestamp__gte=lookback_start,
            timestamp__lt=window_start,
        )
        .extra(select={"hour": "strftime('%%H', timestamp)"})  # noqa: S610 (controlled)
        .values("hour")
        .annotate(c=Count("id"))
    )
    # SQLite/Postgres farqi yo'q bo'lishi uchun sodda usul: o'rtacha soatlik
    total_hist = PageView.objects.filter(
        site=site, timestamp__gte=lookback_start, timestamp__lt=window_start,
    ).count()
    avg_per_hour = total_hist / (LOOKBACK_DAYS * 24) if total_hist else 0

    if avg_per_hour < 5:
        # Yetarlicha tarixiy ma'lumot yo'q — anomaliya tekshirmaymiz
        return None

    delta_pct = ((current - avg_per_hour) / avg_per_hour) * 100
    if abs(delta_pct) < THRESHOLD_PCT:
        return None

    # Dedup: oxirgi soat ichida shu sayt uchun anomaliya bildirishnoma bormi?
    recent_dup = Notification.objects.filter(
        user=site.user,
        site=site,
        type=Notification.Type.ANOMALY,
        created_at__gte=now - timedelta(minutes=DEDUP_WINDOW_MINUTES),
    ).exists()
    if recent_dup:
        return None

    direction = "oshib ketdi" if delta_pct > 0 else "kamaydi"
    title = f"Trafik anomaliyasi: {site.name}"
    message = (
        f"Oxirgi {WINDOW_MINUTES} daqiqada trafik {abs(delta_pct):.0f}% "
        f"{direction}. Hozirgi: {current}, normalda: {avg_per_hour:.0f}/soat."
    )
    return Notification.objects.create(
        user=site.user,
        site=site,
        type=Notification.Type.ANOMALY,
        title=title,
        message=message,
    )


def detect_anomalies() -> int:
    """Hamma faol saytlar uchun anomaliya tekshiruvi (cron job)."""
    created = 0
    for site in Site.objects.filter(is_active=True).select_related("user"):
        try:
            n = detect_for_site(site)
            if n:
                created += 1
                logger.info("Anomaliya bildirishnomasi yaratildi: %s", n.id)
        except Exception:
            logger.exception("Anomaly detect xatosi sayt %s uchun", site.id)
    return created
