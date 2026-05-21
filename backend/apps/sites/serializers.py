"""Site serializers."""
import re

from rest_framework import serializers

from .models import Site


DOMAIN_RE = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.[A-Za-z]{2,}$"
)


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            "id", "name", "domain", "api_key", "is_active",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "api_key", "created_at", "updated_at")

    def validate_domain(self, value: str) -> str:
        value = value.lower().strip()
        # http://, https://, www. ni olib tashlash
        value = re.sub(r"^https?://", "", value)
        value = re.sub(r"^www\.", "", value)
        value = value.rstrip("/")

        if not DOMAIN_RE.match(value):
            raise serializers.ValidationError("Domen formati noto'g'ri (masalan: example.com)")
        return value


class SiteCreateSerializer(SiteSerializer):
    """Sayt yaratish — user'ni avto-attach qilish."""

    def create(self, validated_data: dict) -> Site:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
