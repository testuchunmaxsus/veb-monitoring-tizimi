from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "site", "format", "status", "date_from", "date_to", "created_at")
    list_filter = ("format", "status", "created_at")
    readonly_fields = ("created_at", "completed_at")
