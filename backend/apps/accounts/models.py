"""Foydalanuvchi modeli (email asosida login)."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Email-asosli foydalanuvchi yaratish uchun manager."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra):
        if not email:
            raise ValueError(_("Email majburiy"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email: str, password: str | None = None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    """Email asosli login foydalanadigan foydalanuvchi."""

    username = None  # username olib tashlandi
    email = models.EmailField(_("Email"), unique=True)
    full_name = models.CharField(_("To'liq ism"), max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    def __str__(self) -> str:
        return self.email
