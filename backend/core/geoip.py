"""GeoIP wrapper (MaxMind GeoLite2)."""
from __future__ import annotations

import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

_reader = None


def _get_reader():
    global _reader
    if _reader is not None:
        return _reader

    db_path = Path(settings.GEOIP_DB_PATH)
    if not db_path.exists():
        logger.warning("GeoIP DB topilmadi: %s. Geolokatsiya o'chiq.", db_path)
        return None

    try:
        import geoip2.database

        _reader = geoip2.database.Reader(str(db_path))
        return _reader
    except Exception as exc:
        logger.exception("GeoIP DB ochilmadi: %s", exc)
        return None


def lookup(ip: str) -> dict | None:
    """IP manzilini geolokatsiya ma'lumotlariga aylantiradi.

    Mahalliy IP'lar (127.x, 10.x, 192.168.x) uchun None qaytaradi.
    """
    if not ip or ip.startswith(("127.", "10.", "192.168.", "::1")):
        return None

    reader = _get_reader()
    if reader is None:
        return None

    try:
        resp = reader.city(ip)
        return {
            "country": resp.country.iso_code,
            "country_name": resp.country.name,
            "city": resp.city.name,
            "latitude": resp.location.latitude,
            "longitude": resp.location.longitude,
        }
    except Exception:
        return None
