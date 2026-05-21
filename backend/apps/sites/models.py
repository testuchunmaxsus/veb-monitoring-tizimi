"""Site modeli."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apikey import generate_api_key


class Site(models.Model):
    """Foydalanuvchi tomonidan kuzatilayotgan sayt."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sites",
        verbose_name=_("Egasi"),
    )
    name = models.CharField(_("Nomi"), max_length=255)
    domain = models.CharField(_("Domen"), max_length=255)
    api_key = models.CharField(
        _("API kalit"), max_length=64, unique=True, default=generate_api_key, editable=False,
    )
    is_active = models.BooleanField(_("Faol"), default=True)
    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Sayt")
        verbose_name_plural = _("Saytlar")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["api_key"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.domain})"

    def regenerate_api_key(self) -> str:
        """API kalitni yangilaydi."""
        self.api_key = generate_api_key()
        self.save(update_fields=["api_key", "updated_at"])
        return self.api_key
