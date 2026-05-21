# TEXNIK TOPSHIRIQ

## Veb-sayt faoliyatini monitoring va tahlil qilish axborot tizimini ishlab chiqish

---

**Loyiha nomi:** Veb-Monitoring Tizimi
**Loyiha turi:** Web-ilova (full-stack)
**Versiya:** 1.0
**Sana:** 2026-yil aprel-may
**Tayyorladi:** Ismoilov Javohir Ulug'bek o'g'li
**Rahbar:** Tojimamatov Israil Nurmamatovich
**Kafedra:** Amaliy matematika va informatika
**Universitet:** Farg'ona Davlat Universiteti

---

## 1. UMUMIY MA'LUMOTLAR

### 1.1. Loyihaning maqsadi

Mazkur kurs ishida veb-saytlar faoliyatini real vaqt rejimida kuzatuvchi, foydalanuvchilar xatti-harakatini yig'uvchi, statistik tahlil qiluvchi va vizualizatsiya qiluvchi to'liq full-stack axborot tizimi (Web Analytics Platform) ishlab chiqiladi. Tizim Google Analytics, Plausible Analytics va Umami Analytics kabi xalqaro mahsulotlarning soddalashtirilgan o'zbek tilidagi analogi sifatida ishlab chiqiladi.

### 1.2. Loyihaning vazifalari

1. Tashqi veb-saytlarga o'rnatiladigan engil JavaScript tracker (kuzatuvchi) yaratish.
2. Yig'ilgan ma'lumotlarni qabul qiluvchi va saqlovchi backend xizmat (REST API) ishlab chiqish.
3. Saytlar faoliyati statistikasini tahlil qiluvchi algoritmlar yaratish.
4. Foydalanuvchi do'st bo'lgan, real vaqtda yangilanuvchi vizualizatsiya paneli (dashboard) ishlab chiqish.
5. PDF va CSV formatlarda hisobot eksport qilish funksiyasi.
6. Trafik anomaliyalarini avtomatik aniqlash va bildirishnomalar tizimi.

### 1.3. Loyihaning aktualligi

Bugungi kunda har bir veb-sayt egasi o'z saytining qanday ishlashini, foydalanuvchilar qaysi mamlakatlardan kelishini, qaysi sahifalar mashhurligini va sayt qaysi qurilmalarda yaxshi ko'rinishini bilishni xohlaydi. Mavjud xalqaro yechimlar (Google Analytics) maxfiylik bilan bog'liq muammolarga ega va ko'pincha o'zbek tilini qo'llab-quvvatlamaydi. Mahalliy yechim yaratish maxfiylik, til va texnik suverenitetni ta'minlaydi.

---

## 2. FUNKSIONAL TALABLAR

### 2.1. Foydalanuvchi rollari

| Rol | Tavsif | Imkoniyatlar |
|-----|--------|--------------|
| **Mehmon** | Tizimga kirmagan foydalanuvchi | Bosh sahifa, ro'yxatdan o'tish, kirish |
| **Foydalanuvchi** | Tizimga kirgan, sayt egasi | Saytlarni boshqarish, statistika ko'rish, hisobot olish |
| **Administrator** | Tizim adminstratori | Barcha foydalanuvchilarni va saytlarni boshqarish (Django Admin) |

### 2.2. Funksional talablar ro'yxati

#### F1. Autentifikatsiya tizimi
- F1.1. Email va parol orqali ro'yxatdan o'tish
- F1.2. Email va parol orqali tizimga kirish (login)
- F1.3. JWT (Access + Refresh) token asosida sessiyalarni boshqarish
- F1.4. Parolni o'zgartirish
- F1.5. Tizimdan chiqish (logout)

#### F2. Saytlarni boshqarish
- F2.1. Yangi sayt qo'shish (nom, domen)
- F2.2. Sayt uchun unikal API kalit avtomatik generatsiya qilish
- F2.3. Saytlar ro'yxatini ko'rish
- F2.4. Sayt sozlamalarini tahrirlash
- F2.5. Saytni o'chirish (barcha statistika bilan birga)
- F2.6. Tracker JavaScript kodini ko'rish va nusxa olish

#### F3. Tracker (kuzatuv skript)
- F3.1. Hajmi minified holatda 5 KB dan kam bo'lishi
- F3.2. Sahifa ko'rishini qayd etish (URL, sarlavha, vaqt)
- F3.3. Klik hodisalarini avtomatik yig'ish
- F3.4. Form yuborilishini qayd etish
- F3.5. Performance metrikalarini o'lchash (LCP, FCP, TTFB, sahifa yuklanish vaqti)
- F3.6. Sessiyalarni boshqarish (sessionStorage orqali)
- F3.7. Sahifa yopilganda `navigator.sendBeacon` orqali ma'lumot yuborish
- F3.8. Offline holatda hodisalarni navbatga qo'yish (queue)

#### F4. Ma'lumotlar yig'ish (Backend)
- F4.1. API kalit asosida sayt identifikatsiyasi
- F4.2. IP manzilidan geolokatsiya aniqlash (mamlakat, shahar)
- F4.3. User-Agent header'idan brauzer, OS, qurilma turini aniqlash
- F4.4. Referrer (kim qaysi saytdan kelganini) qayd etish
- F4.5. Bounce rate hisoblash (sessiya = 1 sahifa va < 30 sek)
- F4.6. Sessiya davomiyligini hisoblash
- F4.7. Rate limiting (DDoS himoyasi)

#### F5. Analitika va vizualizatsiya
- F5.1. Umumiy ko'rsatkichlar (jami sahifalar, unikal tashrif buyuruvchilar, sessiyalar, bounce rate)
- F5.2. Vaqt bo'yicha grafik (line chart, soat/kun/oy bo'yicha)
- F5.3. Eng mashhur sahifalar jadvali (top pages)
- F5.4. Eng mashhur referrerlar jadvali (top referrers)
- F5.5. Qurilma turlari bo'yicha bo'linish (mobile/desktop/tablet)
- F5.6. Brauzer va OS statistikasi
- F5.7. Geografik bo'linish (mamlakatlar, shaharlar)
- F5.8. Sahifa heatmap (klik koordinatalari)
- F5.9. Funnel analysis (foydalanuvchi qadam-qadam o'tish jarayoni)
- F5.10. Sana oralig'i bo'yicha filtrlash (preset: bugun, 7 kun, 30 kun, custom)

#### F6. Real-time monitoring
- F6.1. WebSocket orqali jonli ma'lumotlar uzatish
- F6.2. Hozirgi onlayn foydalanuvchilar soni
- F6.3. Real vaqtda hodisalar oqimi (live event feed)
- F6.4. Hozirgi vaqtda ko'rilayotgan sahifalar

#### F7. Hisobotlar
- F7.1. PDF formatda hisobot yaratish
- F7.2. CSV formatda raw ma'lumotlarni eksport qilish
- F7.3. Sana oralig'i va sayt bo'yicha filtrlash
- F7.4. Yaratilgan hisobotlar tarixini saqlash

#### F8. Bildirishnomalar
- F8.1. Trafik anomaliyalarini avtomatik aniqlash (har 5 daqiqada)
- F8.2. Email orqali bildirish
- F8.3. Dashboard ichida real vaqt bildirishnomalar
- F8.4. Bildirishnoma o'qildi belgisi
- F8.5. Bildirishnoma sozlamalari

---

## 3. NOFUNKSIONAL TALABLAR

### 3.1. Ishlash unumdorligi (Performance)

| Parametr | Qiymat |
|----------|--------|
| API javob vaqti (lokal) | < 200 ms |
| Dashboard yangilanish vaqti | < 1 sek |
| Tracker yuklanish vaqti | < 100 ms |
| Tracker hajmi (gzipped) | < 5 KB |
| WebSocket latency | < 500 ms |

### 3.2. Xavfsizlik (Security)

- Parollar `bcrypt` algoritmi orqali hashlangan holda saqlanishi
- JWT tokenlar 60 daqiqa yaroqlilik muddati
- HTTPS qo'llab-quvvatlash (production'da)
- SQL Injection va XSS hujumlarining oldini olish (Django ORM va React eskeyplari orqali)
- CSRF himoya
- Rate limiting (API kalit asosida)
- API kalitlari kamida 32 simvol uzunlikda

### 3.3. Kengayuvchanlik (Scalability)

- Database: SQLite (dev) → PostgreSQL (production)
- Background tasklar uchun django-q2 → Celery + Redis
- Channels: in-memory → Redis backend

### 3.4. Foydalanish qulayligi (Usability)

- Interfeys o'zbek tilida
- Responsive dizayn (mobile, tablet, desktop)
- Loading va error holatlari uchun aniq UI
- Empty state'lar (sayt yo'q, ma'lumot yo'q)

### 3.5. Hujjatlashtirish

- Barcha hujjatlar o'zbek tilida (lotin alifbosi)
- API endpointlari Swagger UI orqali interaktiv hujjatlashtirilgan
- Kod izohlari ingliz tilida (texnik standart)

---

## 4. TIZIM ARXITEKTURASI

### 4.1. Yuqori darajadagi diagramma

```
┌─────────────────────┐
│ Tashqi veb-sayt     │
│ + tracker.min.js    │
└──────────┬──────────┘
           │ HTTP/sendBeacon
           ▼
┌─────────────────────────────────────┐
│ Backend (Django + Channels)         │
│ ┌─────────────┐  ┌────────────────┐ │
│ │ REST API    │  │ WebSocket      │ │
│ │ (DRF)       │  │ (Channels)     │ │
│ └─────────────┘  └────────────────┘ │
│         │                  │        │
│         ▼                  ▼        │
│ ┌─────────────────────────────────┐ │
│ │ Database (SQLite/PostgreSQL)    │ │
│ └─────────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────┐
│ Frontend (React)    │
│ Dashboard           │
└─────────────────────┘
```

### 4.2. Komponentlar

| Komponent | Texnologiya | Vazifa |
|-----------|-------------|--------|
| Tracker | Vanilla TypeScript | Tashqi saytlardan ma'lumot yig'ish |
| Backend API | Django REST Framework | Ma'lumotlarni qabul qilish va xizmat ko'rsatish |
| Real-time | Django Channels + Daphne | WebSocket orqali jonli yangilanishlar |
| Database | SQLite / PostgreSQL | Ma'lumotlarni saqlash |
| Background | django-q2 | Anomaliya tekshiruvi, eski ma'lumotlarni tozalash |
| Frontend | React + Vite + TypeScript | Foydalanuvchi interfeysi |

---

## 5. INSTRUMENTAL VOSITALAR

### 5.1. Backend (Python)

- **Python 3.11+**
- **Django 5.0** — web framework
- **Django REST Framework 3.15** — REST API
- **Django Channels 4.1** — WebSocket
- **Daphne 4.1** — ASGI server
- **SimpleJWT** — JWT autentifikatsiya
- **drf-spectacular** — OpenAPI 3.0 hujjatlash
- **django-q2** — background task queue
- **geoip2** — IP geolokatsiya
- **user-agents** — User-Agent parsing
- **reportlab** — PDF generatsiya
- **pytest-django** — testlar

### 5.2. Frontend (TypeScript)

- **Node.js 20 LTS**
- **React 18** — UI library
- **Vite 5** — build tool
- **TypeScript 5.6** — type safety
- **TailwindCSS 3.4** — utility-first CSS
- **Recharts 2** — chart library
- **TanStack Query 5** — server state
- **Zustand 5** — client state
- **React Router 6** — routing
- **Axios** — HTTP client

### 5.3. Tracker (TypeScript, Vanilla)

- **TypeScript** — type safety
- **Vite library mode** — build
- **Terser** — minification
- Hech qanday runtime dependency yo'q

---

## 6. ISHLAB CHIQISH BOSQICHLARI

| # | Bosqich | Vaqt (soat) |
|---|---------|-------------|
| 0 | Loyiha skeleton | 4-6 |
| 1 | Hujjatlar yozish | 8-10 |
| 2 | Database modellar | 4-5 |
| 3 | Autentifikatsiya | 5-6 |
| 4 | Saytlarni boshqarish | 3-4 |
| 5 | Tracking + Tracker | 8-10 |
| 6 | Analitika moduli | 8-10 |
| 7 | Frontend dashboard | 10-12 |
| 8 | Real-time | 5-6 |
| 9 | Hisobotlar | 5-6 |
| 10 | Bildirishnomalar | 4-5 |
| 11 | Testlar va polish | 6-8 |
| **Jami** | | **70-88** |

---

## 7. NATIJALAR VA YETKAZIB BERILADIGAN MATERIALLAR

### 7.1. Dasturiy ta'minot

1. To'liq ishlovchi backend (REST API + WebSocket)
2. Foydalanuvchi do'st frontend dashboard
3. Tracker JavaScript skript (5 KB dan kam)
4. Database migratsiyalari va seed ma'lumotlari
5. Bir buyruq bilan ishga tushuvchi setup (`start.bat`)

### 7.2. Hujjatlashtirish

1. Texnik topshiriq (TZ) — ushbu hujjat
2. Loyiha rejasi (sprint reja, roadmap)
3. Tizim arxitekturasi
4. Ma'lumotlar bazasi tavsifi
5. API hujjatlari (Swagger orqali interaktiv)
6. Foydalanish qo'llanmasi
7. README

### 7.3. Test natijalari

- Unit testlar (kamida 80% coverage)
- Integration testlar (asosiy flow'lar)
- Manual test natijalari (skrinshotlar)

---

## 8. RIVOJLANTIRISH ISTIQBOLLARI

Loyihaning kelajakdagi rivojlanishi uchun quyidagi imkoniyatlar nazarda tutilgan:

- A/B testing platformasi
- Email kampaniyalar bilan integratsiya
- Mashina o'rganish asosida bashoratli analitika
- Custom event'lar uchun SDK
- Mobile (iOS/Android) tracker SDK
- Plugin tizimi (WordPress, Tilda, Shopify)
- Multi-tenancy (jamoa hisoblari)

---

**Tasdiqlandi:**

| Lavozim | F.I.O. | Imzo | Sana |
|---------|--------|------|------|
| Talaba | Ismoilov Javohir Ulug'bek o'g'li | _____________ | _____________ |
| Rahbar | Tojimamatov Israil Nurmamatovich | _____________ | _____________ |
| Kafedra mudiri | _____________________ | _____________ | _____________ |
