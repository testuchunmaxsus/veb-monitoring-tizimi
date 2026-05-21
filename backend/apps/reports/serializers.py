"""Reports serializers."""
from rest_framework import serializers

from apps.sites.models import Site

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="site.name", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "id", "site", "site_name", "format", "status",
            "date_from", "date_to", "file_url",
            "error_message", "created_at", "completed_at",
        )
        read_only_fields = ("status", "file_url", "error_message", "created_at", "completed_at")

    def get_file_url(self, obj: Report) -> str | None:
        return obj.file.url if obj.file else None


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("site", "format", "date_from", "date_to")

    def validate(self, attrs: dict) -> dict:
        if attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError({"date_from": "Boshlanish sanasi tugash sanasidan keyin"})
        return attrs

    def validate_site(self, value: Site) -> Site:
        request = self.context.get("request")
        if request and value.user_id != request.user.id:
            raise serializers.ValidationError("Bu sayt sizga tegishli emas")
        return value

    def create(self, validated_data: dict) -> Report:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
