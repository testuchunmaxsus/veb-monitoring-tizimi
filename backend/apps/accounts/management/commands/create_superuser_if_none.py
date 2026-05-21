"""Deploy vaqtida superuser yaratish (agar mavjud bo'lmasa)."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = "Superuser mavjud bo'lmasa, env variables'dan yangi superuser yaratadi"

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("Superuser allaqachon mavjud. O'tkazib yuborildi."))
            return

        email = config("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
        password = config("DJANGO_SUPERUSER_PASSWORD", default="admin12345")

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser yaratildi: {email}"))
