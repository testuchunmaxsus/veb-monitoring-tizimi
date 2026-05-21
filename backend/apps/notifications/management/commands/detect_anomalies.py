"""`python manage.py detect_anomalies` — qo'lda anomaliya tekshiruvi.

Production'da django-q2 schedule orqali har 5 daqiqada chaqiriladi.
"""
from django.core.management.base import BaseCommand

from apps.notifications.detectors import detect_anomalies


class Command(BaseCommand):
    help = "Barcha saytlarda trafik anomaliyasini tekshiradi"

    def handle(self, *args, **options) -> None:
        created = detect_anomalies()
        self.stdout.write(self.style.SUCCESS(f"Yaratilgan bildirishnomalar: {created}"))
