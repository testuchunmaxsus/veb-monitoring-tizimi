from django.contrib import admin

from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "user", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "domain", "user__email")
    readonly_fields = ("api_key", "created_at", "updated_at")
