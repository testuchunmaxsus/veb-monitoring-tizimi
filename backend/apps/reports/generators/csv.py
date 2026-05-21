"""CSV hisobot generatori (xom ma'lumotlar)."""
from __future__ import annotations

import csv
import io
from datetime import datetime
from typing import Iterable

from apps.tracking.models import PageView


def generate_csv(*, site_id: int, start: datetime, end: datetime) -> bytes:
    """PageView'larni CSV formatida qaytaradi."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "timestamp", "url", "title", "referrer",
        "country", "city", "browser", "os", "device", "is_mobile",
        "load_time_ms", "lcp_ms", "fcp_ms", "ttfb_ms",
    ])

    qs: Iterable[PageView] = (
        PageView.objects.select_related("session")
        .filter(site_id=site_id, timestamp__gte=start, timestamp__lte=end)
        .order_by("timestamp")
        .iterator(chunk_size=1000)
    )
    for pv in qs:
        s = pv.session
        writer.writerow([
            pv.timestamp.isoformat(),
            pv.url,
            pv.title,
            pv.referrer,
            s.country,
            s.city,
            s.browser,
            s.os,
            s.device,
            s.is_mobile,
            pv.load_time_ms or "",
            pv.lcp_ms or "",
            pv.fcp_ms or "",
            pv.ttfb_ms or "",
        ])
    return buf.getvalue().encode("utf-8")
