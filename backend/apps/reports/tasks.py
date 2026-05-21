"""Hisobot generatsiyasi (django-q2 task uchun mos)."""
from __future__ import annotations

import logging
from datetime import datetime, time

from django.core.files.base import ContentFile
from django.utils import timezone

from .generators.csv import generate_csv
from .generators.pdf import generate_pdf
from .models import Report

logger = logging.getLogger(__name__)


def generate_report(report_id: int) -> None:
    """Sinxron generatsiya — view yoki django-q2 chaqiradi."""
    try:
        report = Report.objects.select_related("site").get(pk=report_id)
    except Report.DoesNotExist:
        logger.warning("Hisobot topilmadi: %s", report_id)
        return

    report.status = Report.Status.PROCESSING
    report.save(update_fields=["status"])

    try:
        tz = timezone.get_current_timezone()
        start = timezone.make_aware(datetime.combine(report.date_from, time.min), tz)
        end = timezone.make_aware(datetime.combine(report.date_to, time.max), tz)

        if report.format == Report.Format.CSV:
            content = generate_csv(site_id=report.site_id, start=start, end=end)
            ext = "csv"
        else:
            content = generate_pdf(site=report.site, start=start, end=end)
            ext = "pdf"

        filename = f"site_{report.site_id}_{report.date_from}_{report.date_to}.{ext}"
        report.file.save(filename, ContentFile(content), save=False)
        report.status = Report.Status.DONE
        report.completed_at = timezone.now()
        report.save()
    except Exception as exc:
        logger.exception("Hisobot generatsiyasi xato: %s", exc)
        report.status = Report.Status.FAILED
        report.error_message = str(exc)[:500]
        report.save(update_fields=["status", "error_message"])
