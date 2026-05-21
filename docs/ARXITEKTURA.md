# TIZIM ARXITEKTURASI

## Veb-Monitoring Tizimi — Texnik arxitektura hujjati

---

## 1. UMUMIY ARXITEKTURA

### 1.1. Yondashuv

Tizim **uch qatlamli (3-tier)** arxitektura asosida qurilgan:

1. **Taqdimot qatlami (Presentation Layer)** — React frontend
2. **Biznes mantiq qatlami (Business Logic Layer)** — Django backend
3. **Ma'lumot qatlami (Data Layer)** — SQLite/PostgreSQL DB

### 1.2. Yuqori darajadagi diagramma

```
┌────────────────────────────────────────────────────────────────┐
│                    FOYDALANUVCHI                               │
└─────────────────────────┬──────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
┌──────────────────────┐    ┌──────────────────────────┐
│ Tashqi veb-saytlar   │    │ Dashboard (Brauzer)      │
│ + tracker.min.js     │    │ React SPA                │
└──────────┬───────────┘    └──────────┬───────────────┘
           │                           │
           │ HTTP POST                 │ HTTP/HTTPS + WebSocket
           │ (sendBeacon/fetch)        │
           │                           │
           └───────────┬───────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │        Daphne (ASGI server)         │
        │             Port 8000               │
        └────────┬───────────────────┬────────┘
                 │                   │
                 ▼                   ▼
        ┌────────────────┐  ┌────────────────┐
        │ Django REST    │  │ Django         │
        │ Framework      │  │ Channels       │
        │ (HTTP)         │  │ (WebSocket)    │
        └────────┬───────┘  └────────┬───────┘
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
        ┌─────────────────────────────────────┐
        │         Django ORM                  │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │ Database                            │
        │ ┌──────────┐    ┌──────────────┐    │
        │ │ SQLite   │ OR │ PostgreSQL   │    │
        │ │ (dev)    │    │ (production) │    │
        │ └──────────┘    └──────────────┘    │
        └─────────────────────────────────────┘

        ┌─────────────────────────────────────┐
        │ Background Worker (django-q2)       │
        │ - Anomaliya detector (cron)         │
        │ - Eski sessiyalarni tozalash        │
        │ - Email yuborish                    │
        └─────────────────────────────────────┘
```

---

## 2. KOMPONENTLAR TAVSIFI

### 2.1. Frontend (React SPA)

**Texnologiyalar:** React 18, TypeScript, Vite, TailwindCSS, Recharts, TanStack Query, Zustand, React Router

**Vazifalari:**
- Foydalanuvchi interfeysi (login, dashboard, sozlamalar)
- Backend API bilan ishlash (REST + WebSocket)
- Server state caching (TanStack Query)
- Client state boshqaruvi (Zustand)
- Real-time yangilanishlar (WebSocket)

**Sahifalar:**

```
/                      → HomePage (mehmon uchun)
/login                 → LoginPage
/register              → RegisterPage
/dashboard             → DashboardPage (umumiy ko'rsatkichlar)
/sites                 → SitesPage (saytlar ro'yxati)
/sites/:id             → SiteDetailsPage (tabs: Overview, Pages, Behavior, Realtime)
/sites/:id/realtime    → RealtimePage (jonli oqim)
/reports               → ReportsPage (PDF/CSV)
/settings              → SettingsPage (profil, sozlamalar)
```

---

### 2.2. Backend (Django + DRF + Channels)

**Texnologiyalar:** Python 3.11, Django 5.0, DRF 3.15, Channels 4, Daphne, SimpleJWT

**Asosiy modullar (apps):**

| App | Vazifasi |
|-----|----------|
| `accounts` | Foydalanuvchilar, autentifikatsiya, JWT |
| `sites` | Saytlarni boshqarish, API kalitlar |
| `tracking` | Public endpoint, ma'lumot yig'ish |
| `analytics` | Aggregation, statistika |
| `reports` | PDF/CSV eksport |
| `notifications` | Anomaliya detector, email |
| `realtime` | WebSocket consumers |

**Modul-modul muloqot:**

```
        ┌─────────────┐
        │   tracking  │ ◄─── Tashqi tracker
        └──────┬──────┘
               │ Event yaratiladi
               ▼
        ┌─────────────┐         ┌──────────────┐
        │   realtime  │ ──────▶ │ WebSocket    │
        │  (broadcast)│         │ subscriber   │
        └─────────────┘         └──────────────┘
               │
               │ Async fonda
               ▼
        ┌─────────────┐
        │ analytics   │ ◄─── Foydalanuvchi dashboard
        └─────────────┘
               │
               ▼
        ┌─────────────┐
        │ notifications│ (anomaliya tekshiruvi cron)
        └─────────────┘
```

---

### 2.3. Tracker (tashqi JS skript)

**Texnologiyalar:** Vanilla TypeScript, Vite library mode

**Vazifalari:**
- Sahifa ko'rishlarini qayd etish
- Klik va form hodisalarini yig'ish
- Performance metrikalarini o'lchash (PerformanceObserver API)
- Ma'lumotlarni backend'ga yuborish

**Hayot sikli:**

```
[Sahifa yuklanadi]
      │
      ▼
[Tracker init]                    ──────► API Key tekshiruvi
      │                                          │
      ▼                                          │
[Session ID hosil qilish]                        │
      │                                          │
      ▼                                          │
[PageView qayd etish] ─────────► POST /track/pageview
      │
      ▼
[Event listenerlar o'rnatish: click, submit]
      │
      ▼
[PerformanceObserver yoqish: LCP, FCP, TTFB]
      │
      ▼
[Kutib turish]
      │
      ▼
[Foydalanuvchi sahifani yopadi]
      │
      ▼
[sendBeacon orqali yakuniy ma'lumot yuborish]
```

---

### 2.4. Database

**Boshlang'ich:** SQLite (zero-config, lokal dev)
**Production:** PostgreSQL (yuqori unumdorlik)

**Asosiy jadvallar:**

```
┌──────────────┐         ┌──────────────┐
│    Users     │◄───────┤    Sites     │
└──────────────┘         └──────┬───────┘
                                │
                ┌───────────────┼─────────────┐
                ▼               ▼             ▼
        ┌──────────────┐ ┌──────────┐ ┌─────────────┐
        │   Sessions   │ │PageViews │ │   Events    │
        └──────────────┘ └──────────┘ └─────────────┘

┌──────────────┐         ┌──────────────┐
│Notifications │         │   Reports    │
└──────────────┘         └──────────────┘
```

To'liq tafsilotlar `MA'LUMOTLAR_BAZASI.md` faylida.

---

### 2.5. Background tasks (django-q2)

**Vazifalari:**
- Anomaliya detection (har 5 daqiqada)
- Eski sessiyalarni tozalash (kuniga 1 marta, 90 kundan eski)
- Email yuborish (asinxron)
- Hisobot generatsiyasi (asinxron)

---

## 3. MA'LUMOT OQIMI (DATA FLOW)

### 3.1. Tracking flow (sahifa ko'rishi)

```
[Foydalanuvchi tashqi saytga kiradi]
              │
              ▼
[Brauzer tracker.min.js'ni yuklaydi]
              │
              ▼
[Tracker pageview event yaratadi]
              │
              │ POST /api/v1/track/pageview
              │ { api_key, url, title, referrer, session_id }
              ▼
[Backend tracking.views.PageViewCreateView]
              │
              ├─► API kalit tekshiruvi (Site model)
              ├─► IP'dan geolokatsiya (geoip2)
              ├─► UA parsing (user-agents)
              ├─► Session DB'da saqlash yoki yangilash
              └─► PageView DB'da saqlash
              │
              ▼
[Channel layer'ga broadcast]
              │
              ▼
[WebSocket consumers o'sha site uchun emit]
              │
              ▼
[Dashboard real vaqtda yangilanadi]
```

### 3.2. Dashboard flow (statistika ko'rish)

```
[Foydalanuvchi dashboard ochadi]
              │
              ▼
[React App auth tekshiruvi (Zustand)]
              │
              ▼
[TanStack Query GET /api/v1/analytics/overview?from=...&to=...]
              │
              ▼
[Backend analytics.views.OverviewView]
              │
              ├─► JWT tekshiruvi
              ├─► Saytga ruxsat tekshiruvi
              ├─► Cache lookup (in-memory LRU)
              ├─► DB query (Session.objects.filter(...))
              ├─► Aggregation (count, avg, distinct)
              └─► JSON javob
              │
              ▼
[React Recharts orqali vizualizatsiya]
              │
              ▼
[Foydalanuvchi grafikni ko'radi]
```

### 3.3. Real-time flow (WebSocket)

```
[Dashboard ochilgach]
        │
        ▼
[useSocket hook ulanadi: ws://localhost:8000/ws/site/{id}/]
        │
        ▼
[Channels JWT cookie/header tekshiradi]
        │
        ▼
[SiteConsumer.connect() chaqiriladi]
        │
        ▼
[Group'ga qo'shiladi: site_{id}]
        │
        ▼
[Online users counter +1]
        │
        ▼
[Yangi tracking event kelgach]
        │
        ▼
[group_send → barcha consumers oladi]
        │
        ▼
[Frontend voqealar oqimida ko'rsatadi]
```

---

## 4. XAVFSIZLIK ARXITEKTURASI

### 4.1. Autentifikatsiya

- **JWT tokenlar:** Access (60 daq), Refresh (7 kun)
- Refresh token rotatsiyasi va blacklist
- Parollar: bcrypt (Django default), 8+ simvol

### 4.2. Avtorizatsiya

- DRF permission'lar: `IsAuthenticated`, `IsOwner`
- Site-level access control: foydalanuvchi faqat o'z saytlarini ko'radi
- Admin panel: faqat staff foydalanuvchilar

### 4.3. Tracking endpoint himoyasi

- API kalit asosida (32 simvol urlsafe)
- Rate limiting: 10 000 /min per API key
- CORS: `Allow-Origin: *` faqat `/track/*` uchun
- IP hashing (SHA-256) — raw IP saqlanmaydi

### 4.4. CSRF, XSS, SQL Injection

- CSRF: Django default (cookie + middleware)
- XSS: React default escape, DRF JSON
- SQL Injection: Django ORM (parameterized)

---

## 5. UNUMDORLIK STRATEGIYALARI

### 5.1. Caching

| Joy | Strategiya | TTL |
|-----|-----------|-----|
| Analytics overview | In-memory LRU | 60 sek |
| Top pages | In-memory LRU | 60 sek |
| Geo lookup | Module-level | session davomida |
| User profile | Frontend (Zustand) | sessiya |

### 5.2. Database optimizatsiyasi

- Indekslar: `(site_id, timestamp)`, `session_id`
- WAL mode (SQLite)
- Connection pooling (PostgreSQL)
- Bulk inserts

### 5.3. Frontend

- Code splitting (route-based)
- Lazy loading
- TanStack Query caching
- Memoization (React.memo)

---

## 6. KENGAYUVCHANLIK (SCALABILITY)

### 6.1. Vertikal kengayish

- SQLite → PostgreSQL
- In-memory cache → Redis
- In-memory channels → Redis channels

### 6.2. Gorizontal kengayish

- Bir nechta Daphne instance + load balancer (nginx)
- Redis pub/sub Channels uchun
- Celery workers (django-q2 o'rniga)

---

## 7. DEPLOYMENT ARXITEKTURASI

### 7.1. Lokal (dev)

```
[Windows/macOS/Linux]
      │
      ├── Daphne (port 8000)
      │      └── Django (DEBUG=True)
      │             └── SQLite (db.sqlite3)
      │
      └── Vite dev server (port 5173)
             └── React (HMR)
```

### 7.2. Production (kelajakda)

```
[Linux server]
      │
      ├── nginx (port 80/443)
      │     ├── Static files (React build)
      │     └── Proxy → Daphne workers
      │
      ├── Daphne x N (port 8001-8003)
      │     └── Django (DEBUG=False)
      │           └── PostgreSQL (separate server)
      │
      ├── Redis (channels + cache)
      │
      └── django-q2 cluster
            └── Background tasks
```

---

## 8. MUVAFFAQIYAT MEZONLARI

| Mezon | Maqsad |
|-------|--------|
| Tracker hajmi | < 5 KB gzipped |
| API javob vaqti | < 200 ms (lokal) |
| Dashboard yuklanish | < 2 sek |
| Test coverage | ≥ 80% |
| Real-time latency | < 500 ms |
| Uptime (production) | ≥ 99% |

---

## 9. RIVOJLANTIRISH ISTIQBOLLARI

- Multi-tenancy (jamoa hisoblari)
- Mobil ilova (React Native)
- ML asosida bashoratli analitika
- A/B testing
- WordPress plugin
- Custom event SDK
