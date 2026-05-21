"""Online users (presence) hisoblash — in-memory."""
from __future__ import annotations

from collections import defaultdict
from threading import Lock


class PresenceRegistry:
    """Sayt ID -> hozir ulangan WebSocket sessiyalar soni.

    In-memory; production'da Redis bilan almashtirish kerak.
    """

    def __init__(self) -> None:
        self._counts: dict[int, int] = defaultdict(int)
        self._lock = Lock()

    def join(self, site_id: int) -> int:
        with self._lock:
            self._counts[site_id] += 1
            return self._counts[site_id]

    def leave(self, site_id: int) -> int:
        with self._lock:
            self._counts[site_id] = max(self._counts[site_id] - 1, 0)
            return self._counts[site_id]

    def get(self, site_id: int) -> int:
        return self._counts.get(site_id, 0)


presence = PresenceRegistry()
