"""Notifications serializers."""
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="site.name", read_only=True, default=None)

    class Meta:
        model = Notification
        fields = (
            "id", "type", "title", "message", "site", "site_name",
            "is_read", "created_at",
        )
        read_only_fields = fields
