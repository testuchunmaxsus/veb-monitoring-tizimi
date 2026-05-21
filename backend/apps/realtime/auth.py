"""WebSocket uchun JWT autentifikatsiya middleware."""
from __future__ import annotations

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def _get_user(user_id: int):
    try:
        return User.objects.get(pk=user_id, is_active=True)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """`?token=<access>` query param'idan JWT'ni o'qiydi."""

    async def __call__(self, scope, receive, send):
        query = parse_qs(scope.get("query_string", b"").decode())
        token = (query.get("token") or [None])[0]

        scope["user"] = AnonymousUser()
        if token:
            try:
                access = AccessToken(token)
                user_id = access.get("user_id")
                if user_id:
                    scope["user"] = await _get_user(user_id)
            except (TokenError, InvalidToken):
                pass
        return await super().__call__(scope, receive, send)
