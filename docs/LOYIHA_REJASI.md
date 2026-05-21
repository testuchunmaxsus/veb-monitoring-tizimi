# LOYIHA REJASI

## Veb-Monitoring Tizimi — Bajarish rejasi

---

## 1. KIRISH

### 1.1. Loyihaning umumiy tavsifi

Mazkur loyiha kurs ishi doirasida bajarilayotgan amaliy ish bo'lib, veb-saytlar faoliyatini real vaqt rejimida monitoring qilish va tahlil qilish uchun mo'ljallangan to'liq full-stack axborot tizimini ishlab chiqishni o'z ichiga oladi.

### 1.2. Asosiy mezonlar

| Mezon | Qiymat |
|-------|--------|
| Boshlanish sanasi | 2026-yil 2-mart |
| Tugash sanasi | 2026-yil 11-may |
| Himoya sanasi | 2026-yil 16-may |
| Jami ish hajmi | 70-88 soat |
| Hafta soni | ~10 hafta |

---

## 2. ISHLAB CHIQISH METODOLOGIYASI

### 2.1. Tanlangan metodologiya

Loyiha **Iterativ-Incremental** metodologiya asosida olib boriladi. Har bir bosqich (sprint) mustaqil mahsulot (deliverable) yaratadi va keyingi bosqichga asos bo'ladi.

### 2.2. Asosiy printsiplar

- **TDD (Test-Driven Development)** — kritik modullar uchun
- **DRY (Don't Repeat Yourself)** — kod qayta ishlatish
- **KISS (Keep It Simple, Stupid)** — sodda yechimlar
- **YAGNI (You Aren't Gonna Need It)** — keraksiz funksiyalardan voz kechish
- **Documentation-first** — har bir bosqich uchun avval hujjat

---

## 3. SPRINT REJASI

### Sprint 0 — Loyiha asoslarini tashkil qilish (1 hafta)

**Davri:** 2026-03-02 — 2026-03-08
**Vaqt:** 4-6 soat

**Vazifalar:**
- [x] Loyiha papkasi tuzilishini yaratish
- [x] Git repository (ixtiyoriy)
- [x] Backend skeleton (Django + DRF + Channels)
- [x] Frontend skeleton (React + Vite + Tailwind)
- [x] Tracker skeleton (Vite library mode)
- [x] `start.bat` skripti
- [x] `.env.example` fayllar
- [x] README.md

**Deliverable:** `start.bat` ishga tushirilganda backend (8000) va frontend (5173) ishlay oladigan bo'sh skelet.

---

### Sprint 1 — Hujjatlashtirish (1 hafta)

**Davri:** 2026-03-09 — 2026-03-15
**Vaqt:** 8-10 soat

**Vazifalar:**
- [x] TEXNIK_TOPSHIRIQ.md
- [x] LOYIHA_REJASI.md (ushbu hujjat)
- [x] ARXITEKTURA.md
- [x] MA'LUMOTLAR_BAZASI.md
- [x] API_DOCS.md
- [x] FOYDALANISH_QOLLANMASI.md

**Deliverable:** 7 ta to'liq texnik hujjat, kurs ishi 1-2 boblariga to'g'ridan-to'g'ri ko'chirib ishlatilishi mumkin.

---

### Sprint 2 — Ma'lumotlar bazasi va modellar (1 hafta)

**Davri:** 2026-03-16 — 2026-03-22
**Vaqt:** 4-5 soat

**Vazifalar:**
- [ ] User modeli (custom email-based)
- [ ] Site modeli (API kalit bilan)
- [ ] Session, PageView, Event modellari
- [ ] Notification modeli
- [ ] Report modeli
- [ ] Migratsiyalar yaratish
- [ ] Indekslar qo'shish
- [ ] Seed skript (demo ma'lumotlar)

**Deliverable:** `python manage.py migrate` muvaffaqiyatli bajariladi. Admin panel orqali ma'lumotlar ko'riladi.

---

### Sprint 3 — Autentifikatsiya tizimi (1 hafta)

**Davri:** 2026-03-23 — 2026-03-29
**Vaqt:** 5-6 soat

**Vazifalar:**
- [ ] Register endpoint (email + parol)
- [ ] Login endpoint (JWT issue)
- [ ] Refresh token endpoint
- [ ] `/me` endpoint
- [ ] Logout (token blacklist)
- [ ] Frontend Login/Register sahifalari
- [ ] Auth store (Zustand + persist)
- [ ] Protected routes wrapper
- [ ] Axios interceptor

**Deliverable:** Foydalanuvchi ro'yxatdan o'tadi, kiradi va dashboard'ga o'tadi.

---

### Sprint 4 — Saytlarni boshqarish (3-4 kun)

**Davri:** 2026-03-30 — 2026-04-02
**Vaqt:** 3-4 soat

**Vazifalar:**
- [ ] Site CRUD endpointlari
- [ ] API kalit generatsiyasi
- [ ] Frontend SitesPage
- [ ] "Sayt qo'shish" modal
- [ ] Tracker snippet copy-to-clipboard
- [ ] Sayt o'chirish tasdiqlash

**Deliverable:** Foydalanuvchi sayt qo'sha oladi va tracker kodini olib, o'z saytiga joylab oladi.

---

### Sprint 5 — Tracking endpointlar va Tracker (1.5 hafta)

**Davri:** 2026-04-03 — 2026-04-12
**Vaqt:** 8-10 soat

**Vazifalar:**
- [ ] `/track/pageview` endpoint
- [ ] `/track/event` endpoint
- [ ] `/track/session/end` endpoint
- [ ] Geo IP integratsiyasi
- [ ] UA parsing
- [ ] Bounce rate logikasi
- [ ] Tracker core class
- [ ] Pageview, click, form, performance collectorlari
- [ ] Transport (sendBeacon + fetch)
- [ ] Build optimizatsiyasi (5KB dan kam)

**Deliverable:** Tashqi sayt `tracker.min.js`'ni yuklaydi va ma'lumotlar backend'da yoziladi.

---

### Sprint 6 — Analitika moduli (1.5 hafta)

**Davri:** 2026-04-13 — 2026-04-22
**Vaqt:** 8-10 soat

**Vazifalar:**
- [ ] `/analytics/overview` endpoint
- [ ] `/analytics/timeseries` endpoint
- [ ] `/analytics/top-pages` endpoint
- [ ] `/analytics/top-referrers` endpoint
- [ ] `/analytics/devices` endpoint
- [ ] `/analytics/geo` endpoint
- [ ] Date range filter
- [ ] In-memory caching

**Deliverable:** API orqali barcha statistik ma'lumotlar olinadi va testlangan.

---

### Sprint 7 — Frontend dashboard (1.5 hafta)

**Davri:** 2026-04-23 — 2026-05-02
**Vaqt:** 10-12 soat

**Vazifalar:**
- [ ] AppShell, Sidebar, Topbar
- [ ] DashboardPage
- [ ] SiteDetailsPage (tabs: Overview, Pages, Behavior, Realtime)
- [ ] LineChart, BarChart, PieChart komponentlari
- [ ] MetricCard komponenti
- [ ] DateRangePicker
- [ ] Top Pages jadvali
- [ ] Geo breakdown
- [ ] Loading va error states

**Deliverable:** Foydalanuvchi to'liq, chiroyli dashboard'da statistikani ko'radi.

---

### Sprint 8 — Real-time (3-4 kun)

**Davri:** 2026-05-03 — 2026-05-06
**Vaqt:** 5-6 soat

**Vazifalar:**
- [ ] Channels consumer
- [ ] JWT-based WebSocket auth
- [ ] Site rooms
- [ ] Tracking endpoint'da broadcast
- [ ] Online users counter
- [ ] Frontend `useSocket` hook
- [ ] RealtimePage

**Deliverable:** Dashboard'da real vaqtda yangi tashriflar ko'rinadi.

---

### Sprint 9 — Hisobotlar (3 kun)

**Davri:** 2026-05-07 — 2026-05-09
**Vaqt:** 5-6 soat

**Vazifalar:**
- [ ] PDF generator (reportlab)
- [ ] CSV generator
- [ ] Reports list endpoint
- [ ] File download endpoint
- [ ] Frontend ReportsPage

**Deliverable:** Foydalanuvchi PDF va CSV hisobot yuklab olishi mumkin.

---

### Sprint 10 — Bildirishnomalar (2-3 kun)

**Davri:** 2026-05-09 — 2026-05-11
**Vaqt:** 4-5 soat

**Vazifalar:**
- [ ] Anomaly detector (django-q2 cron)
- [ ] Notification yaratish
- [ ] Email yuborish
- [ ] WebSocket push
- [ ] Frontend bildirishnomalar dropdown

**Deliverable:** Anomaliyalar avtomatik aniqlanadi va bildirishnoma yuboriladi.

---

### Sprint 11 — Testlar va polishing (2-3 kun)

**Davri:** 2026-05-11 — 2026-05-13
**Vaqt:** 6-8 soat

**Vazifalar:**
- [ ] Backend unit testlar (80% coverage)
- [ ] Integration testlar
- [ ] Frontend smoke testlar
- [ ] Bug fix sprint
- [ ] README final
- [ ] Demo screenshot'lar
- [ ] Kurs ishi tushuntirish xati
- [ ] Taqdimot slaydlari

**Deliverable:** Loyiha himoyaga to'liq tayyor.

---

## 4. RISKLAR REESTRI

| # | Risk | Ehtimollik | Ta'sir | Qarshi chora |
|---|------|-----------|--------|--------------|
| R1 | Vaqt yetishmasligi | O'rta | Yuqori | MVP-first yondashuv, ixtiyoriy fazalarni oxirida |
| R2 | Tracker hajmi 5KB dan oshishi | O'rta | O'rta | Vanilla TS, tree-shaking, terser passes:3 |
| R3 | CORS muammolari | Yuqori | Yuqori | `/track/*` faqat origin:* ruxsat |
| R4 | SQLite konkurensiyasi | O'rta | Past (lokal) | WAL mode, batch inserts |
| R5 | localhost'da geo ishlamasligi | Yuqori | Past | Dev rejimda fake IP fallback |
| R6 | Talaba React/TS bilmasligi | O'rta | Yuqori | Sodda patternlar, ko'p izoh, video tutoriallar |
| R7 | Kompyuter ishlamay qolishi | Past | Yuqori | Git/cloud backup |
| R8 | Rahbar vaqtida bo'lmasligi | O'rta | O'rta | Hafta boshida statusni yuborish |

---

## 5. RESURSLAR

### 5.1. Inson resurslari

- **Talaba:** Ismoilov Javohir Ulug'bek o'g'li (asosiy ishlab chiquvchi)
- **Rahbar:** Tojimamatov Israil Nurmamatovich (maslahat, tekshirish)
- **AI yordamchi:** Claude Code (kod yozishda yordam)

### 5.2. Texnik resurslar

- **Apparat:** Shaxsiy kompyuter (Windows 10, 8GB+ RAM)
- **Dasturiy ta'minot:**
  - Python 3.11+
  - Node.js 20 LTS
  - VS Code yoki PyCharm
  - Git
  - Brauzer (Chrome, Firefox)

### 5.3. Bilim resurslari

- Django rasmiy hujjatlari: https://docs.djangoproject.com/
- React hujjatlari: https://react.dev/
- DRF hujjatlari: https://www.django-rest-framework.org/
- TypeScript handbook: https://www.typescriptlang.org/docs/

---

## 6. SIFAT MEZONLARI

### 6.1. Kod sifati

| Mezon | Qiymat |
|-------|--------|
| Test coverage (backend) | ≥ 80% |
| Funksiya uzunligi | < 50 satr |
| Fayl uzunligi | < 800 satr |
| Cyclomatic complexity | < 10 |
| Komment darajasi | Kerakli joylarda |

### 6.2. Performance

| Mezon | Qiymat |
|-------|--------|
| API javob (P95) | < 500 ms |
| Dashboard FCP | < 1.5 sek |
| Tracker hajmi | < 5 KB |
| WebSocket latency | < 500 ms |

---

## 7. YAKUNIY NATIJALAR (DELIVERABLES)

Loyiha tugagandan so'ng quyidagi materiallar topshiriladi:

### 7.1. Dasturiy ta'minot
- ✅ Backend manba kodi (Django + DRF + Channels)
- ✅ Frontend manba kodi (React + Vite + Tailwind)
- ✅ Tracker manba kodi va build natijasi
- ✅ `start.bat` setup skripti
- ✅ Demo ma'lumotlar (seed)

### 7.2. Hujjatlar
- ✅ TEXNIK_TOPSHIRIQ.md
- ✅ LOYIHA_REJASI.md
- ✅ ARXITEKTURA.md
- ✅ MA'LUMOTLAR_BAZASI.md
- ✅ API_DOCS.md
- ✅ FOYDALANISH_QOLLANMASI.md
- ✅ README.md

### 7.3. Kurs ishi
- ✅ Tushuntirish xati (DOCX)
- ✅ Taqdimot slaydlari (PPTX)
- ✅ Demo skrinshotlar

---

## 8. KENGAYTIRISH IMKONIYATLARI

Loyihaning kelajakdagi versiyalarida amalga oshirilishi mumkin:

- Mobil ilova (React Native)
- A/B testing platformasi
- Mashina o'rganish asosida bashoratli analitika
- WordPress va Shopify pluginlari
- Multi-tenancy (jamoa hisoblari)
- Custom event SDK (kutubxona shaklida)

---

**Reja tasdiqlandi:**

Talaba: ________________ Sana: __________
Rahbar: ________________ Sana: __________
