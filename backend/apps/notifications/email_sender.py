"""Bildirishnomalar uchun email yuborish."""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import Notification

logger = logging.getLogger(__name__)


def send_notification_email(notification: Notification) -> bool:
    """Bildirishnomani email orqali yuboradi (best-effort)."""
    user = notification.user
    if not user.email:
        return False
    body = (
        f"{notification.message}\n\n"
        f"Dashboard: {settings.FRONTEND_URL}/notifications\n"
    )
    try:
        send_mail(
            subject=f"[Veb-Monitoring] {notification.title}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return True
    except Exception:
        logger.exception("Email yuborish xato")
        return False
