"""Tracking serializers (public endpointlar uchun)."""
from rest_framework import serializers


class PageViewIngestSerializer(serializers.Serializer):
    """Tracker'dan keladigan sahifa ko'rishi payload."""

    api_key = serializers.CharField(max_length=64)
    session_uid = serializers.CharField(max_length=64)
    url = serializers.CharField(max_length=2000)
    title = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")
    referrer = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")
    load_time_ms = serializers.IntegerField(required=False, min_value=0, max_value=600000, allow_null=True)
    lcp_ms = serializers.IntegerField(required=False, min_value=0, max_value=600000, allow_null=True)
    fcp_ms = serializers.IntegerField(required=False, min_value=0, max_value=600000, allow_null=True)
    ttfb_ms = serializers.IntegerField(required=False, min_value=0, max_value=600000, allow_null=True)


class EventIngestSerializer(serializers.Serializer):
    """Custom event payload."""

    api_key = serializers.CharField(max_length=64)
    session_uid = serializers.CharField(max_length=64)
    type = serializers.ChoiceField(choices=["click", "form", "scroll", "custom"])
    target = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")
    metadata = serializers.JSONField(required=False, default=dict)


class SessionEndSerializer(serializers.Serializer):
    """Sessiya tugashini bildiruvchi payload."""

    api_key = serializers.CharField(max_length=64)
    session_uid = serializers.CharField(max_length=64)
    duration_sec = serializers.IntegerField(min_value=0, max_value=86400, required=False, default=0)
