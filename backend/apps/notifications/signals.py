"""Bildirishnoma yaratilgach email yuborish va WebSocket'ga push."""
from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.realtime.broadcast import broadcast_event

from .email_sender import send_notification_email
from .models import Notification


@receiver(post_save, sender=Notification)
def on_notification_created(sender, instance: Notification, created: bool, **kwargs) -> None:
    if not created:
        return

    # Email yuborish (faqat anomaly va warning'lar uchun)
    if instance.type in (Notification.Type.ANOMALY, Notification.Type.WARNING):
        send_notification_email(instance)

    # WebSocket push (agar sayt mavjud bo'lsa)
    if instance.site_id:
        broadcast_event(
            site_id=instance.site_id,
            event_type="notification",
            payload={
                "id": instance.id,
                "type": instance.type,
                "title": instance.title,
                "message": instance.message,
                "created_at": instance.created_at.isoformat(),
            },
        )
