"""Analytics endpointlari uchun umumiy filter yordamchilari."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Optional

from django.utils import timezone
from rest_framework.exceptions import ValidationError


@dataclass
class DateRange:
    """Sana oralig'i (timezone-aware)."""

    start: datetime
    end: datetime

    @property
    def days(self) -> int:
        return max((self.end - self.start).days, 1)


def parse_date(value: Optional[str], default: date) -> date:
    if not value:
        return default
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError({"date": f"Sana noto'g'ri: {value}"}) from exc


def get_date_range(query_params, default_days: int = 7) -> DateRange:
    """`from` va `to` query param'larini tahlil qiladi.

    Default: oxirgi `default_days` kun (bugun shu kunni ham o'z ichiga oladi).
    """
    today = timezone.localdate()
    start_date = parse_date(query_params.get("from"), today - timedelta(days=default_days - 1))
    end_date = parse_date(query_params.get("to"), today)
    if start_date > end_date:
        raise ValidationError({"date": "from sanasi to sanasidan keyin bo'lmasligi kerak"})

    tz = timezone.get_current_timezone()
    start_dt = timezone.make_aware(datetime.combine(start_date, time.min), tz)
    end_dt = timezone.make_aware(datetime.combine(end_date, time.max), tz)
    return DateRange(start=start_dt, end=end_dt)


def get_previous_range(rng: DateRange) -> DateRange:
    """Solishtirish uchun avvalgi davr."""
    delta = rng.end - rng.start
    return DateRange(start=rng.start - delta, end=rng.start)
