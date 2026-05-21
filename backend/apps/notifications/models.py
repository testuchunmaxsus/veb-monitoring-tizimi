"""Bildirishnoma modeli."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class Type(models.TextChoices):
        ANOMALY = "anomaly", _("Anomaliya")
        INFO = "info", _("Ma'lumot")
        WARNING = "warning", _("Ogohlantirish")
        SUCCESS = "success", _("Muvaffaqiyat")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="notifications",
    )
    type = models.CharField(_("Turi"), max_length=32, choices=Type.choices, default=Type.INFO)
    title = models.CharField(_("Sarlavha"), max_length=255)
    message = models.TextField(_("Matn"))
    is_read = models.BooleanField(_("O'qilgan"), default=False)
    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)

    class Meta:
        verbose_name = _("Bildirishnoma")
        verbose_name_plural = _("Bildirishnomalar")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"[{self.type}] {self.title}"
