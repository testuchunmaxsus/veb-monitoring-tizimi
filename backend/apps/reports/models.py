"""Hisobot modeli."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    class Format(models.TextChoices):
        PDF = "pdf", "PDF"
        CSV = "csv", "CSV"

    class Status(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        PROCESSING = "processing", _("Bajarilmoqda")
        DONE = "done", _("Tayyor")
        FAILED = "failed", _("Xato")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="reports",
    )
    format = models.CharField(_("Format"), max_length=8, choices=Format.choices)
    status = models.CharField(
        _("Holat"), max_length=16, choices=Status.choices, default=Status.PENDING,
    )
    date_from = models.DateField(_("Sana boshi"))
    date_to = models.DateField(_("Sana oxiri"))
    file = models.FileField(_("Fayl"), upload_to="reports/%Y/%m/", blank=True, null=True)
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    completed_at = models.DateTimeField(_("Tugatilgan"), null=True, blank=True)

    class Meta:
        verbose_name = _("Hisobot")
        verbose_name_plural = _("Hisobotlar")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.format.upper()} hisobot #{self.id}"
