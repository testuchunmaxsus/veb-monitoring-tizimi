"""WebSocket consumers."""
from __future__ import annotations

import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.sites.models import Site

from .broadcast import site_group
from .presence import presence

logger = logging.getLogger(__name__)


class SiteConsumer(AsyncJsonWebsocketConsumer):
    """Sayt uchun real-time hodisalar oqimi.

    URL: /ws/site/<site_id>/?token=<access>
    """

    site_id: int | None = None

    async def connect(self) -> None:
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        try:
            self.site_id = int(self.scope["url_route"]["kwargs"]["site_id"])
        except (KeyError, ValueError):
            await self.close(code=4400)
            return

        owns = await self._user_owns_site(user.id, self.site_id)
        if not owns:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(site_group(self.site_id), self.channel_name)
        await self.accept()

        count = presence.join(self.site_id)
        await self.channel_layer.group_send(
            site_group(self.site_id),
            {"type": "broadcast.message", "event_type": "presence", "payload": {"online": count}},
        )

    async def disconnect(self, code: int) -> None:
        if self.site_id is None:
            return
        await self.channel_layer.group_discard(site_group(self.site_id), self.channel_name)
        count = presence.leave(self.site_id)
        try:
            await self.channel_layer.group_send(
                site_group(self.site_id),
                {"type": "broadcast.message", "event_type": "presence", "payload": {"online": count}},
            )
        except Exception:
            pass

    async def receive_json(self, content, **kwargs) -> None:
        # Hozircha clientdan xabarlarni qabul qilmaymiz; ping/pong default
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def broadcast_message(self, event: dict) -> None:
        """`group_send` orqali kelgan xabarni clientga uzatadi."""
        await self.send_json(
            {
                "type": event.get("event_type", "message"),
                "data": event.get("payload", {}),
            }
        )

    @staticmethod
    @database_sync_to_async
    def _user_owns_site(user_id: int, site_id: int) -> bool:
        return Site.objects.filter(pk=site_id, user_id=user_id).exists()
