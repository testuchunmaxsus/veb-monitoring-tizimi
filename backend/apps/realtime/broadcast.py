"""Channels group_send helper (HTTP view'lardan WebSocket'ga emit qilish)."""
from __future__ import annotations

import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


def site_group(site_id: int) -> str:
    return f"site_{site_id}"


def broadcast_event(*, site_id: int, event_type: str, payload: dict) -> None:
    """Sayt room'iga real-time hodisa yuborish.

    Channels layer mavjud bo'lmasa (test rejimda) — sukut bilan o'tib ketadi.
    """
    layer = get_channel_layer()
    if layer is None:
        return
    try:
        async_to_sync(layer.group_send)(
            site_group(site_id),
            {"type": "broadcast.message", "event_type": event_type, "payload": payload},
        )
    except Exception:
        logger.exception("Broadcast xatosi (sayt %s)", site_id)
