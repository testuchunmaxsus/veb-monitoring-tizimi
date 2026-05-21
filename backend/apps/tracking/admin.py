from django.contrib import admin

from .models import Event, PageView, Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "country_code", "browser", "os", "is_mobile", "started_at", "is_bounce")
    list_filter = ("is_mobile", "is_bot", "is_bounce", "country_code", "browser", "os")
    search_fields = ("session_uid", "site__name", "country", "city")
    readonly_fields = tuple(f.name for f in Session._meta.fields if f.name != "id")
    date_hierarchy = "started_at"


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("url", "site", "timestamp", "load_time_ms")
    list_filter = ("site", "timestamp")
    search_fields = ("url", "title")
    readonly_fields = tuple(f.name for f in PageView._meta.fields if f.name != "id")
    date_hierarchy = "timestamp"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("type", "target", "site", "timestamp")
    list_filter = ("type", "site", "timestamp")
    search_fields = ("target",)
    readonly_fields = tuple(f.name for f in Event._meta.fields if f.name != "id")
    date_hierarchy = "timestamp"
