"""Kurs ishi uchun diagrammalar generator."""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"


def architecture_diagram() -> None:
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    boxes = [
        # (x, y, w, h, label, color)
        (1, 8, 3, 1.4, "Tashqi veb-saytlar\n+ tracker.min.js", "#fde68a"),
        (10, 8, 3, 1.4, "Dashboard (Brauzer)\nReact SPA", "#bfdbfe"),
        (5, 5.5, 4, 1.4, "Daphne ASGI server\n(port 8000)", "#a7f3d0"),
        (1, 3, 3.5, 1.4, "Django REST API\n(DRF)", "#ddd6fe"),
        (9, 3, 3.5, 1.4, "Django Channels\n(WebSocket)", "#fecaca"),
        (5, 0.5, 4, 1.4, "Database\nSQLite / PostgreSQL", "#f5d0fe"),
    ]
    for x, y, w, h, t, c in boxes:
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.05",
            linewidth=1.5, facecolor=c, edgecolor="#374151",
        ))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center",
                fontsize=10, fontweight="bold")

    arrows = [
        (2.5, 8, 6.5, 6.4, "HTTP POST\nsendBeacon"),
        (11.5, 8, 7.5, 6.4, "HTTP/WebSocket"),
        (6.5, 5.5, 2.7, 4.4, ""),
        (7.5, 5.5, 10.7, 4.4, ""),
        (2.7, 3, 6.5, 1.9, ""),
        (10.7, 3, 7.5, 1.9, ""),
    ]
    for x1, y1, x2, y2, lbl in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#6b7280", lw=1.5))
        if lbl:
            ax.text((x1 + x2) / 2 + 0.3, (y1 + y2) / 2,
                    lbl, fontsize=8, color="#6b7280")

    ax.set_title("Veb-Monitoring Tizimi: umumiy arxitektura",
                 fontsize=13, fontweight="bold", pad=12)
    plt.savefig(os.path.join(OUT, "architecture.png"), dpi=150, bbox_inches="tight")
    plt.close()


def er_diagram() -> None:
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    tables = {
        "User":      (0.5, 7.5, ["id (PK)", "email (UNIQUE)", "password", "full_name", "date_joined"]),
        "Site":      (5.0, 7.5, ["id (PK)", "user_id (FK)", "name", "domain", "api_key (UNIQUE)", "is_active"]),
        "Session":   (10.0, 8.0, ["id (PK)", "site_id (FK)", "session_uid", "ip_hash", "country", "browser", "started_at"]),
        "PageView":  (5.0, 3.5, ["id (PK)", "site_id (FK)", "session_id (FK)", "url", "title", "load_time_ms", "timestamp"]),
        "Event":     (10.0, 3.5, ["id (PK)", "site_id (FK)", "session_id (FK)", "type", "target", "metadata", "timestamp"]),
        "Notification": (0.5, 3.5, ["id (PK)", "user_id (FK)", "site_id (FK)", "type", "title", "is_read"]),
    }
    coords = {}
    for name, (x, y, fields) in tables.items():
        h = 0.4 + 0.32 * (len(fields) + 1)
        ax.add_patch(mpatches.Rectangle((x, y - h), 3.5, h,
                                        linewidth=1.5, facecolor="#eff6ff",
                                        edgecolor="#1e40af"))
        ax.add_patch(mpatches.Rectangle((x, y - 0.4), 3.5, 0.4,
                                        linewidth=0, facecolor="#1e40af"))
        ax.text(x + 1.75, y - 0.2, name, ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
        for i, fld in enumerate(fields):
            ax.text(x + 0.15, y - 0.6 - i * 0.32, fld,
                    ha="left", va="center", fontsize=8)
        coords[name] = (x + 1.75, y - h / 2 - 0.2, x, x + 3.5, y - h, y)

    rels = [
        ("User", "Site"),
        ("Site", "Session"),
        ("Site", "PageView"),
        ("Site", "Event"),
        ("Session", "PageView"),
        ("Session", "Event"),
        ("User", "Notification"),
        ("Site", "Notification"),
    ]
    for a, b in rels:
        cx_a = coords[a][0]
        cx_b = coords[b][0]
        cy_a = coords[a][1]
        cy_b = coords[b][1]
        ax.plot([cx_a, cx_b], [cy_a, cy_b], color="#9ca3af",
                linestyle="--", linewidth=1, alpha=0.6)

    ax.set_title("Ma'lumotlar bazasi ER diagrammasi",
                 fontsize=13, fontweight="bold", pad=10)
    plt.savefig(os.path.join(OUT, "er.png"), dpi=150, bbox_inches="tight")
    plt.close()


def dataflow_diagram() -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis("off")

    steps = [
        (0.3, "Foydalanuvchi\nsaytga kiradi"),
        (2.7, "tracker.min.js\nyuklanadi"),
        (5.1, "PageView\npayload"),
        (7.5, "Backend\nqabul qiladi"),
        (9.9, "DB ga yoziladi\nva broadcast"),
        (12.3, "Dashboard\nreal vaqtda"),
    ]
    for x, t in steps:
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, 2), 2.0, 1.4, boxstyle="round,pad=0.05",
            linewidth=1.5, facecolor="#dbeafe", edgecolor="#1e40af",
        ))
        ax.text(x + 1.0, 2.7, t, ha="center", va="center", fontsize=9)
    for x, _ in steps[:-1]:
        ax.annotate("", xy=(x + 2.4, 2.7), xytext=(x + 2.0, 2.7),
                    arrowprops=dict(arrowstyle="->", color="#1e40af", lw=2))

    ax.set_title("Ma'lumot oqimi: tracker → backend → dashboard",
                 fontsize=13, fontweight="bold", pad=10)
    plt.savefig(os.path.join(OUT, "dataflow.png"), dpi=150, bbox_inches="tight")
    plt.close()


def tech_stack_diagram() -> None:
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis("off")

    layers = [
        (0.5, 4, 4, "Frontend qatlami",
         "React 18 + Vite\nTypeScript + TailwindCSS\nRecharts + TanStack Query\nZustand + React Router", "#bfdbfe"),
        (5, 4, 4, "Backend qatlami",
         "Django 5.0 + DRF\nDjango Channels + Daphne\nSimpleJWT + drf-spectacular\ndjango-q2 + reportlab", "#a7f3d0"),
        (9.5, 4, 4, "Tracker qatlami",
         "Vanilla TypeScript\nVite library mode\nZero dependency\n2.16 KB gzipped", "#fde68a"),
        (0.5, 0.3, 13, "Ma'lumot qatlami",
         "SQLite (dev) / PostgreSQL (prod)  •  Django ORM  •  WAL mode  •  Indekslar (site_id+timestamp)",
         "#ddd6fe"),
    ]
    for x, y, w, title, body, c in layers:
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y), w, 1.7, boxstyle="round,pad=0.05",
            linewidth=1.5, facecolor=c, edgecolor="#374151",
        ))
        ax.text(x + w / 2, y + 1.45, title, ha="center", va="center",
                fontsize=11, fontweight="bold")
        ax.text(x + w / 2, y + 0.7, body, ha="center", va="center", fontsize=9)

    ax.set_title("Texnologik stack: 4-qatlamli arxitektura",
                 fontsize=13, fontweight="bold", pad=10)
    plt.savefig(os.path.join(OUT, "tech_stack.png"), dpi=150, bbox_inches="tight")
    plt.close()


def url_routing_diagram() -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis("off")
    rows = [
        ("/api/v1/auth/", "JWT auth (register, login, refresh, me, logout)"),
        ("/api/v1/sites/", "Saytlarni boshqarish (CRUD + API key regenerate)"),
        ("/api/v1/track/pageview/", "Public: sahifa ko'rishi qabul qilish"),
        ("/api/v1/track/event/", "Public: klik va form event'lari"),
        ("/api/v1/track/session/end/", "Public: sessiya yakuni (sendBeacon target)"),
        ("/api/v1/analytics/overview/", "Umumiy ko'rsatkichlar"),
        ("/api/v1/analytics/timeseries/", "Vaqt bo'yicha grafik"),
        ("/api/v1/analytics/top-pages/", "Eng mashhur sahifalar"),
        ("/api/v1/analytics/devices/", "Qurilma/brauzer/OS bo'linishi"),
        ("/api/v1/analytics/geo/", "Geografik bo'linish"),
        ("/api/v1/reports/", "Hisobotlar (PDF/CSV)"),
        ("/api/v1/notifications/", "Bildirishnomalar"),
        ("/ws/site/<id>/", "WebSocket: real-time hodisalar"),
        ("/admin/", "Django admin paneli"),
        ("/api/docs/", "Swagger UI interaktiv hujjatlash"),
    ]
    headers = ["URL marshrut", "Tavsif"]
    cell_text = [list(r) for r in rows]
    table = ax.table(
        cellText=cell_text, colLabels=headers, loc="center",
        cellLoc="left", colWidths=[0.35, 0.65],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.5)
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_facecolor("#1e40af")
            cell.set_text_props(color="white", fontweight="bold")
        elif i % 2 == 0:
            cell.set_facecolor("#f9fafb")
    ax.set_title("Tizim REST API marshrutlari", fontsize=13, fontweight="bold", pad=12)
    plt.savefig(os.path.join(OUT, "url_routing.png"), dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    architecture_diagram()
    er_diagram()
    dataflow_diagram()
    tech_stack_diagram()
    url_routing_diagram()
    print("Diagrammalar tayyor:", OUT)
    for f in os.listdir(OUT):
        print(" -", f)
