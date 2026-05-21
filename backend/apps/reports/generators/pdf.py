"""PDF hisobot generatori (reportlab)."""
from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from apps.analytics import aggregations
from apps.analytics.filters import DateRange
from apps.sites.models import Site


def generate_pdf(*, site: Site, start: datetime, end: datetime) -> bytes:
    """Sayt uchun PDF hisobot."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Hisobot - {site.name}",
    )

    styles = getSampleStyleSheet()
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    body = styles["BodyText"]

    story = []
    story.append(Paragraph(f"Hisobot: {site.name}", h1))
    story.append(Paragraph(f"Domen: {site.domain}", body))
    story.append(Paragraph(
        f"Davr: {start.strftime('%Y-%m-%d')} → {end.strftime('%Y-%m-%d')}",
        body,
    ))
    story.append(Spacer(1, 0.5 * cm))

    rng = DateRange(start=start, end=end)

    # Overview
    ov = aggregations.overview(site.id, rng)
    story.append(Paragraph("Umumiy ko'rsatkichlar", h2))
    story.append(_kv_table([
        ("Sahifa ko'rishlari", str(ov["total_pageviews"])),
        ("Tashrif buyuruvchilar", str(ov["unique_visitors"])),
        ("Sessiyalar", str(ov["total_sessions"])),
        ("Bounce rate", f"{ov['bounce_rate'] * 100:.1f}%"),
        ("O'rtacha sessiya", f"{ov['avg_session_duration_sec']} sek"),
    ]))
    story.append(Spacer(1, 0.5 * cm))

    # Top pages
    top = aggregations.top_pages(site.id, rng, limit=10)
    if top:
        story.append(Paragraph("Eng mashhur sahifalar", h2))
        rows = [["URL", "Sarlavha", "Ko'rishlar", "Tashriflar"]]
        for p in top:
            rows.append([
                _truncate(p["url"], 40),
                _truncate(p["title"], 30),
                str(p["views"]),
                str(p["unique_visitors"]),
            ])
        story.append(_data_table(rows))
        story.append(Spacer(1, 0.5 * cm))

    # Top referrers
    refs = aggregations.top_referrers(site.id, rng, limit=10)
    if refs:
        story.append(Paragraph("Manbalar (Referrers)", h2))
        rows = [["Manba", "Tashriflar"]]
        for r in refs:
            rows.append([_truncate(r["referrer"], 50), str(r["visits"])])
        story.append(_data_table(rows))
        story.append(Spacer(1, 0.5 * cm))

    # Geo
    geo = aggregations.geo(site.id, rng, limit=10)
    if geo["by_country"]:
        story.append(Paragraph("Mamlakatlar bo'yicha", h2))
        rows = [["Kod", "Nom", "Tashriflar"]]
        for c in geo["by_country"]:
            rows.append([c["code"], c["name"], str(c["visits"])])
        story.append(_data_table(rows))
        story.append(Spacer(1, 0.5 * cm))

    # Devices
    dev = aggregations.devices(site.id, rng)
    story.append(Paragraph("Qurilmalar", h2))
    if dev["by_browser"]:
        rows = [["Brauzer", "Soni"]]
        for b in dev["by_browser"][:5]:
            rows.append([b["name"], str(b["count"])])
        story.append(_data_table(rows))

    doc.build(story)
    return buf.getvalue()


def _kv_table(rows: list[tuple[str, str]]) -> Table:
    t = Table(rows, colWidths=[6 * cm, 8 * cm])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def _data_table(rows: list[list[str]]) -> Table:
    t = Table(rows, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _truncate(s: str, n: int) -> str:
    s = s or ""
    return s if len(s) <= n else s[: n - 3] + "..."
