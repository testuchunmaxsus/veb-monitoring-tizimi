"""Tracking modellari: Session, PageView, Event."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Session(models.Model):
    """Tashrif buyuruvchi sessiyasi."""

    site = models.ForeignKey(
        "sites.Site", on_delete=models.CASCADE, related_name="sessions",
    )
    session_uid = models.CharField(_("Session UID"), max_length=64, db_index=True)
    ip_hash = models.CharField(_("IP hash"), max_length=64)

    # Geolokatsiya
    country = models.CharField(_("Mamlakat"), max_length=64, blank=True, default="")
    country_code = models.CharField(_("Mamlakat kodi"), max_length=2, blank=True, default="")
    city = models.CharField(_("Shahar"), max_length=64, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Qurilma
    browser = models.CharField(_("Brauzer"), max_length=64, blank=True, default="")
    browser_version = models.CharField(max_length=32, blank=True, default="")
    os = models.CharField(_("OS"), max_length=64, blank=True, default="")
    os_version = models.CharField(max_length=32, blank=True, default="")
    device = models.CharField(_("Qurilma"), max_length=64, blank=True, default="")
    is_mobile = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)

    # Manba
    referrer = models.CharField(max_length=500, blank=True, default="")

    # Vaqt
    started_at = models.DateTimeField(_("Boshlandi"), auto_now_add=True)
    ended_at = models.DateTimeField(_("Tugadi"), null=True, blank=True)

    # Aggregatsiya
    is_bounce = models.BooleanField(_("Bounce"), default=False)
    page_count = models.PositiveIntegerField(_("Sahifalar soni"), default=1)
    duration_sec = models.PositiveIntegerField(_("Davomiyligi"), null=True, blank=True)

    class Meta:
        verbose_name = _("Sessiya")
        verbose_name_plural = _("Sessiyalar")
        ordering = ("-started_at",)
        indexes = [
            models.Index(fields=["site", "-started_at"]),
            models.Index(fields=["session_uid"]),
            models.Index(fields=["country_code"]),
        ]

    def __str__(self) -> str:
        return f"Session #{self.id} ({self.country_code or 'XX'})"


class PageView(models.Model):
    """Sahifa ko'rishi."""

    site = models.ForeignKey(
        "sites.Site", on_delete=models.CASCADE, related_name="pageviews",
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="pageviews",
    )
    url = models.CharField(_("URL"), max_length=2000)
    title = models.CharField(_("Sarlavha"), max_length=500, blank=True, default="")
    referrer = models.CharField(max_length=500, blank=True, default="")

    # Performance metrikalari (millisekundda)
    load_time_ms = models.PositiveIntegerField(null=True, blank=True)
    lcp_ms = models.PositiveIntegerField(null=True, blank=True, help_text="Largest Contentful Paint")
    fcp_ms = models.PositiveIntegerField(null=True, blank=True, help_text="First Contentful Paint")
    ttfb_ms = models.PositiveIntegerField(null=True, blank=True, help_text="Time To First Byte")

    timestamp = models.DateTimeField(_("Vaqt"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Sahifa ko'rishi")
        verbose_name_plural = _("Sahifa ko'rishlari")
        ordering = ("-timestamp",)
        indexes = [
            models.Index(fields=["site", "-timestamp"]),
            models.Index(fields=["session"]),
        ]

    def __str__(self) -> str:
        return f"{self.url} @ {self.timestamp:%Y-%m-%d %H:%M}"


class Event(models.Model):
    """Custom hodisa: klik, form yuborish, custom event."""

    class EventType(models.TextChoices):
        CLICK = "click", _("Klik")
        FORM = "form", _("Form yuborish")
        CUSTOM = "custom", _("Custom")
        SCROLL = "scroll", _("Scroll")

    site = models.ForeignKey(
        "sites.Site", on_delete=models.CASCADE, related_name="events",
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="events",
    )
    type = models.CharField(_("Turi"), max_length=32, choices=EventType.choices)
    target = models.CharField(_("Maqsad"), max_length=500, blank=True, default="")
    metadata = models.JSONField(_("Qo'shimcha"), default=dict, blank=True)
    timestamp = models.DateTimeField(_("Vaqt"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Hodisa")
        verbose_name_plural = _("Hodisalar")
        ordering = ("-timestamp",)
        indexes = [
            models.Index(fields=["site", "-timestamp"]),
            models.Index(fields=["session"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self) -> str:
        return f"{self.type}: {self.target[:30]}"
