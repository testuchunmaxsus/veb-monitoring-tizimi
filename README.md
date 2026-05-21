# Veb-Sayt Faoliyatini Monitoring va Tahlil Qilish Axborot Tizimi

> **Kurs ishi** — Farg'ona Davlat Universiteti, Amaliy matematika va informatika kafedrasi.
> Talaba: **Ismoilov Javohir Ulug'bek o'g'li** (23.12 guruh, 3-kurs).
> Rahbar: **Tojimamatov Israil Nurmamatovich**.

## Loyiha haqida

Veb-saytlar faoliyatini real vaqt rejimida kuzatuvchi va tahlil qiluvchi to'liq full-stack axborot tizimi. Google Analytics, Plausible va Umami kabi mahsulotlarning soddalashtirilgan o'zbek tilidagi analogi.

## Imkoniyatlar

- **Tracker** — tashqi saytlarga o'rnatiladigan engil JavaScript skript (~5 KB)
- Sahifa ko'rishlari, sessiyalar, klik va form yuborishlarini yig'ish
- Performance metrikalari (LCP, FCP, TTFB, sahifa yuklanish vaqti)
- IP asosida geolokatsiya, qurilma/brauzer/OT aniqlash
- **Real-time** dashboard (Django Channels + WebSocket)
- 4 ta tab bilan sayt tafsilotlari (Umumiy, Sahifalar, Qurilmalar, Geografiya)
- Charts: line, bar, pie + top pages, top referrers, geo, devices jadvallar
- Bir foydalanuvchi bir nechta sayt boshqarishi
- JWT autentifikatsiya (access + refresh)
- **PDF va CSV** hisobotlar (reportlab)
- **Anomaliya detector** + email + dashboard bildirishnomalar

## Texnologiyalar

| Qatlam | Stack |
|--------|-------|
| **Backend** | Python 3.11, Django 5.0, DRF, Channels 4, Daphne, SimpleJWT, drf-spectacular |
| **Database** | SQLite (default) yoki PostgreSQL |
| **Real-time** | Django Channels + WebSocket |
| **Frontend** | React 18, Vite, TypeScript, TailwindCSS, Recharts, TanStack Query, Zustand |
| **Tracker** | Vanilla TypeScript, Vite library mode (zero dependency) |
| **Background** | django-q2 (SQLite-friendly) |
| **PDF/CSV** | reportlab + Python `csv` |

## Ishga tushirish

### Bir buyruq bilan setup (Windows)

```batch
setup.bat
```

Bu skript:
1. Python virtual environment yaratadi
2. Backend dependencies o'rnatadi
3. Migratsiyalarni qo'llaydi
4. Frontend dependencies o'rnatadi
5. Tracker'ni build qiladi

### Qo'lda setup

#### Backend

```batch
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

Demo ma'lumotlar uchun:
```batch
python manage.py shell < scripts\seed.py
```
> Login: `demo@example.com` / `demo1234`

#### Frontend

```batch
cd frontend
npm install
copy .env.example .env
```

#### Tracker

```batch
cd tracker
npm install
npm run build
```

### Ishga tushirish

```batch
start.bat
```

Yoki alohida terminallarda:

```batch
:: Terminal 1 (Backend)
cd backend
venv\Scripts\activate
daphne -b 0.0.0.0 -p 8000 config.asgi:application

:: Terminal 2 (Frontend)
cd frontend
npm run dev
```

## URL'lar

| Xizmat | URL |
|--------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/v1/ |
| **Swagger UI** (interaktiv) | http://localhost:8000/api/docs/ |
| ReDoc | http://localhost:8000/api/redoc/ |
| **Admin panel** | http://localhost:8000/admin/ |
| WebSocket | ws://localhost:8000/ws/site/{id}/ |

## Loyiha tuzilishi

```
Javohir\
├── README.md
├── start.bat / start.sh         # Front+back ishga tushirish
├── setup.bat                    # Bir buyruq bilan o'rnatish
├── package.json                 # Root workspace (concurrently)
│
├── docs\                        # 6 ta o'zbekcha hujjat (~75 KB)
│   ├── TEXNIK_TOPSHIRIQ.md
│   ├── LOYIHA_REJASI.md
│   ├── ARXITEKTURA.md
│   ├── MA'LUMOTLAR_BAZASI.md
│   ├── API_DOCS.md
│   └── FOYDALANISH_QOLLANMASI.md
│
├── backend\                     # Django + Channels
│   ├── config\                  # settings (base/dev/prod), urls, asgi, wsgi
│   ├── apps\
│   │   ├── accounts\            # User + JWT auth
│   │   ├── sites\               # Site CRUD + API key
│   │   ├── tracking\            # Public ingest endpoints
│   │   ├── analytics\           # Aggregation queries
│   │   ├── reports\             # PDF + CSV
│   │   ├── notifications\       # Anomaly + email
│   │   └── realtime\            # Channels WS
│   ├── core\                    # geoip, ua_parser, apikey, pagination
│   ├── scripts\seed.py          # Demo ma'lumotlar
│   ├── conftest.py              # pytest fixtures
│   └── requirements.txt
│
├── frontend\                    # React + Vite + TypeScript
│   └── src\
│       ├── api\                 # Typed API clients
│       ├── components\          # UI, charts, analytics, layout
│       ├── pages\               # 8 ta sahifa
│       ├── hooks\               # useSocket
│       ├── store\               # Zustand auth
│       └── lib\                 # constants, format
│
└── tracker\                     # Vanilla TS, Vite library mode
    └── src\
        ├── core\                # tracker, session, transport
        ├── collectors\          # pageview, click, form, performance
        └── utils\               # uuid
```

## Asosiy foydalanish

1. **Ro'yxatdan o'ting** → http://localhost:5173/register
2. **Sayt qo'shing** → "Sayt qo'shish" tugmasi
3. **Tracker kodini oling** → site cardidagi "Kod" tugmasi
4. **Saytingiz HTML'iga joylang** (head ichiga)
5. **Saytingizga kiring** → Dashboard real vaqtda yangilanadi
6. **Hisobot oling** → Hisobotlar sahifasida PDF/CSV yarating

## Test

```batch
cd backend
venv\Scripts\activate
pytest -v
pytest --cov=apps --cov-report=term-missing  # coverage bilan
```

## Anomaliya detector (qo'lda)

```batch
cd backend
python manage.py detect_anomalies
```

Production'da `django-q2 schedule` orqali har 5 daqiqada chaqirish kerak.

## Hujjatlar

Batafsil:
- [Texnik topshiriq](docs/TEXNIK_TOPSHIRIQ.md) — kurs ishi 2-bobi uchun
- [Loyiha rejasi](docs/LOYIHA_REJASI.md) — sprintlar, risklar
- [Tizim arxitekturasi](docs/ARXITEKTURA.md) — diagrammalar
- [Ma'lumotlar bazasi](docs/MA'LUMOTLAR_BAZASI.md) — ER + jadvallar
- [API hujjatlari](docs/API_DOCS.md) — barcha endpointlar
- [Foydalanish qo'llanmasi](docs/FOYDALANISH_QOLLANMASI.md) — to'liq guide

## Litsenziya

O'quv maqsadlarida ishlab chiqilgan. FarDU 2025-2026 o'quv yili kurs ishi.
