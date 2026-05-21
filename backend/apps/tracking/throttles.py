"""Tracking endpoints uchun rate limiting (API key asosida)."""
from rest_framework.throttling import SimpleRateThrottle


class TrackingRateThrottle(SimpleRateThrottle):
    """Per-API-key rate limit: 10 000/min."""

    scope = "tracking"

    def get_cache_key(self, request, view):
        api_key = (
            request.data.get("api_key")
            if hasattr(request, "data")
            else None
        )
        if not api_key:
            return None
        return self.cache_format % {"scope": self.scope, "ident": api_key}
