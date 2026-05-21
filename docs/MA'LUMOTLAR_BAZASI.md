# MA'LUMOTLAR BAZASI

## Veb-Monitoring Tizimi — Database loyihasi

---

## 1. UMUMIY MA'LUMOTLAR

### 1.1. Ma'lumotlar bazasi tanlovi

Loyihada ikkita ma'lumotlar bazasi qo'llab-quvvatlanadi:

| DBMS | Holat | Vaziyat |
|------|-------|---------|
| **SQLite 3** | Default | Lokal dev, kichik loyihalar |
| **PostgreSQL 14+** | Optional | Production, yuqori yuk |

DBMS tanlovi `DATABASE_URL` muhit o'zgaruvchisi orqali boshqariladi:
- `sqlite:///db.sqlite3` → SQLite
- `postgres://user:pass@host:5432/db` → PostgreSQL

### 1.2. ORM

Django ORM ishlatiladi. Migratsiyalar `python manage.py migrate` orqali boshqariladi.

### 1.3. Normalizatsiya darajasi

Ma'lumotlar bazasi **3NF (3-normal forma)** ga keltirilgan. Faqat tezkor o'qish uchun `Session` jadvalida ba'zi denormalize maydonlar mavjud (country, browser, os) — bu analitik so'rovlarni tezlashtiradi.

---

## 2. ENTITY-RELATIONSHIP DIAGRAMMASI

```
┌──────────────────────────────────┐
│           User                   │
├──────────────────────────────────┤
│ PK id                BIGINT      │
│    email             VARCHAR(254)│ UNIQUE
│    password          VARCHAR(128)│
│    full_name         VARCHAR(255)│
│    is_active         BOOLEAN     │
│    is_staff          BOOLEAN     │
│    date_joined       TIMESTAMPTZ │
│    last_login        TIMESTAMPTZ │
└────────────┬─────────────────────┘
             │ 1
             │
             │ N
┌────────────┴─────────────────────┐
│           Site                   │
├──────────────────────────────────┤
│ PK id                BIGINT      │
│ FK user_id           BIGINT      │
│    name              VARCHAR(255)│
│    domain            VARCHAR(255)│
│    api_key           VARCHAR(64) │ UNIQUE
│    is_active         BOOLEAN     │
│    created_at        TIMESTAMPTZ │
│    updated_at        TIMESTAMPTZ │
└────────────┬─────────────────────┘
             │ 1
             │
             │ N
        ┌────┴────────────┐
        │                 │
        ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│    Session       │  │   PageView       │
├──────────────────┤  ├──────────────────┤
│ PK id            │  │ PK id            │
│ FK site_id       │  │ FK site_id       │
│    session_uid   │  │ FK session_id    │
│    ip_hash       │  │    url           │
│    country       │  │    title         │
│    country_code  │  │    referrer      │
│    city          │  │    load_time_ms  │
│    latitude      │  │    lcp_ms        │
│    longitude     │  │    fcp_ms        │
│    browser       │  │    ttfb_ms       │
│    browser_ver   │  │    timestamp     │
│    os            │  └──────────────────┘
│    os_version    │
│    device        │  ┌──────────────────┐
│    is_mobile     │  │     Event        │
│    is_bot        │  ├──────────────────┤
│    referrer      │  │ PK id            │
│    started_at    │  │ FK site_id       │
│    ended_at      │  │ FK session_id    │
│    is_bounce     │  │    type          │
│    page_count    │  │    target        │
│    duration_sec  │  │    metadata JSON │
└──────────────────┘  │    timestamp     │
                      └──────────────────┘

┌──────────────────────────────────┐
│       Notification               │
├──────────────────────────────────┤
│ PK id                BIGINT      │
│ FK user_id           BIGINT      │
│ FK site_id           BIGINT NULL │
│    type              VARCHAR(32) │
│    title             VARCHAR(255)│
│    message           TEXT        │
│    is_read           BOOLEAN     │
│    created_at        TIMESTAMPTZ │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│          Report                  │
├──────────────────────────────────┤
│ PK id                BIGINT      │
│ FK user_id           BIGINT      │
│ FK site_id           BIGINT      │
│    format            VARCHAR(8)  │ pdf/csv
│    date_from         DATE        │
│    date_to           DATE        │
│    file              VARCHAR(255)│
│    created_at        TIMESTAMPTZ │
└──────────────────────────────────┘
```

---

## 3. JADVALLAR TAVSIFI

### 3.1. `accounts_user`

Tizim foydalanuvchilari. Email asosida login.

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL | Email manzili |
| `password` | VARCHAR(128) | NOT NULL | bcrypt hash |
| `full_name` | VARCHAR(255) | NULL | To'liq ism |
| `is_active` | BOOLEAN | DEFAULT TRUE | Faolligi |
| `is_staff` | BOOLEAN | DEFAULT FALSE | Admin paneliga kirish |
| `is_superuser` | BOOLEAN | DEFAULT FALSE | To'liq huquq |
| `date_joined` | TIMESTAMPTZ | NOT NULL | Ro'yxatdan o'tish vaqti |
| `last_login` | TIMESTAMPTZ | NULL | Oxirgi kirish |

**Indekslar:**
- `email` (UNIQUE)

---

### 3.2. `sites_site`

Foydalanuvchi tomonidan qo'shilgan saytlar.

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `user_id` | BIGINT | FK → User, NOT NULL | Egasi |
| `name` | VARCHAR(255) | NOT NULL | Sayt nomi |
| `domain` | VARCHAR(255) | NOT NULL | Domen (example.com) |
| `api_key` | VARCHAR(64) | UNIQUE, NOT NULL | Tracking uchun kalit (vmt_xxx) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Tracking yoqilgan |
| `created_at` | TIMESTAMPTZ | AUTO | Yaratilgan vaqt |
| `updated_at` | TIMESTAMPTZ | AUTO | O'zgartirilgan vaqt |

**Indekslar:**
- `user_id`
- `api_key` (UNIQUE)
- `domain`

---

### 3.3. `tracking_session`

Tashrif buyuruvchining sessiyasi (browser).

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `site_id` | BIGINT | FK → Site, NOT NULL | Sayt |
| `session_uid` | VARCHAR(64) | NOT NULL | Brauzer tomonidan generated UUID |
| `ip_hash` | VARCHAR(64) | NOT NULL | SHA-256 IP hash (privacy) |
| `country` | VARCHAR(64) | NULL | Mamlakat nomi |
| `country_code` | VARCHAR(2) | NULL | ISO 3166-1 alpha-2 |
| `city` | VARCHAR(64) | NULL | Shahar |
| `latitude` | FLOAT | NULL | Geolokatsiya |
| `longitude` | FLOAT | NULL | Geolokatsiya |
| `browser` | VARCHAR(64) | NULL | Brauzer (Chrome, Firefox) |
| `browser_version` | VARCHAR(32) | NULL | Versiya |
| `os` | VARCHAR(64) | NULL | OS (Windows, Android) |
| `os_version` | VARCHAR(32) | NULL | OS versiya |
| `device` | VARCHAR(64) | NULL | Qurilma turi |
| `is_mobile` | BOOLEAN | DEFAULT FALSE | Mobile/tablet |
| `is_bot` | BOOLEAN | DEFAULT FALSE | Bot ekanligi |
| `referrer` | VARCHAR(500) | NULL | Qaysi saytdan keldi |
| `started_at` | TIMESTAMPTZ | NOT NULL | Sessiya boshlandi |
| `ended_at` | TIMESTAMPTZ | NULL | Sessiya tugadi |
| `is_bounce` | BOOLEAN | DEFAULT FALSE | Bounce sessiya |
| `page_count` | INTEGER | DEFAULT 1 | Ko'rilgan sahifalar soni |
| `duration_sec` | INTEGER | NULL | Davomiyligi (soniyada) |

**Indekslar:**
- `(site_id, started_at)` — vaqt bo'yicha so'rovlar uchun
- `session_uid`
- `country_code`

---

### 3.4. `tracking_pageview`

Sahifa ko'rishlari.

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `site_id` | BIGINT | FK → Site, NOT NULL | Sayt |
| `session_id` | BIGINT | FK → Session, NOT NULL | Sessiya |
| `url` | VARCHAR(2000) | NOT NULL | Sahifa URL'i |
| `title` | VARCHAR(500) | NULL | Sahifa sarlavhasi |
| `referrer` | VARCHAR(500) | NULL | Oldingi sahifa |
| `load_time_ms` | INTEGER | NULL | Yuklanish vaqti (ms) |
| `lcp_ms` | INTEGER | NULL | Largest Contentful Paint |
| `fcp_ms` | INTEGER | NULL | First Contentful Paint |
| `ttfb_ms` | INTEGER | NULL | Time To First Byte |
| `timestamp` | TIMESTAMPTZ | NOT NULL | Sodir bo'lgan vaqt |

**Indekslar:**
- `(site_id, timestamp)` — top pages uchun
- `session_id`

---

### 3.5. `tracking_event`

Custom hodisalar (klik, form, custom).

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `site_id` | BIGINT | FK → Site, NOT NULL | Sayt |
| `session_id` | BIGINT | FK → Session, NOT NULL | Sessiya |
| `type` | VARCHAR(32) | NOT NULL | click/form/custom |
| `target` | VARCHAR(500) | NULL | CSS selector yoki nom |
| `metadata` | JSON | NULL | Qo'shimcha ma'lumotlar |
| `timestamp` | TIMESTAMPTZ | NOT NULL | Sodir bo'lgan vaqt |

**Indekslar:**
- `(site_id, timestamp)`
- `session_id`
- `type`

---

### 3.6. `notifications_notification`

Tizim bildirishnomalari.

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `user_id` | BIGINT | FK → User, NOT NULL | Qabul qiluvchi |
| `site_id` | BIGINT | FK → Site, NULL | Tegishli sayt |
| `type` | VARCHAR(32) | NOT NULL | anomaly/info/warning |
| `title` | VARCHAR(255) | NOT NULL | Sarlavha |
| `message` | TEXT | NOT NULL | Matn |
| `is_read` | BOOLEAN | DEFAULT FALSE | O'qilgan |
| `created_at` | TIMESTAMPTZ | NOT NULL | Yaratilgan |

**Indekslar:**
- `(user_id, is_read)` — o'qilmaganlar uchun
- `(user_id, created_at)`

---

### 3.7. `reports_report`

Generatsiya qilingan hisobotlar.

| Maydon | Tip | Cheklov | Tavsif |
|--------|-----|---------|--------|
| `id` | BIGINT | PK, AUTO | Birlamchi kalit |
| `user_id` | BIGINT | FK → User, NOT NULL | Foydalanuvchi |
| `site_id` | BIGINT | FK → Site, NOT NULL | Sayt |
| `format` | VARCHAR(8) | NOT NULL | pdf/csv |
| `date_from` | DATE | NOT NULL | Sana boshi |
| `date_to` | DATE | NOT NULL | Sana oxiri |
| `file` | VARCHAR(255) | NOT NULL | Saqlash yo'li |
| `created_at` | TIMESTAMPTZ | NOT NULL | Yaratilgan |

**Indekslar:**
- `(user_id, created_at)`

---

## 4. ALOQALAR (RELATIONSHIPS)

| Manba | Qabul | Tip | ON DELETE |
|-------|-------|-----|-----------|
| User | Site | 1:N | CASCADE |
| Site | Session | 1:N | CASCADE |
| Site | PageView | 1:N | CASCADE |
| Site | Event | 1:N | CASCADE |
| Session | PageView | 1:N | CASCADE |
| Session | Event | 1:N | CASCADE |
| User | Notification | 1:N | CASCADE |
| Site | Notification | 1:N | SET NULL |
| User | Report | 1:N | CASCADE |
| Site | Report | 1:N | CASCADE |

---

## 5. INDEKSLAR STRATEGIYASI

### 5.1. Asosiy so'rov uslublari

Loyihada ikki asosiy so'rov uslubi mavjud:

1. **Tracking write** (yuqori chastota): `INSERT INTO PageView, Event, Session`
2. **Analytics read** (past-o'rta chastota): `SELECT ... GROUP BY ... WHERE timestamp BETWEEN ...`

### 5.2. Indekslar tanlovi

```sql
-- Vaqt asosida filter (top pages, timeseries)
CREATE INDEX idx_pageview_site_time ON tracking_pageview (site_id, timestamp DESC);
CREATE INDEX idx_event_site_time ON tracking_event (site_id, timestamp DESC);
CREATE INDEX idx_session_site_time ON tracking_session (site_id, started_at DESC);

-- Sessiya bo'yicha join
CREATE INDEX idx_pageview_session ON tracking_pageview (session_id);
CREATE INDEX idx_event_session ON tracking_event (session_id);

-- Geo so'rovlar
CREATE INDEX idx_session_country ON tracking_session (country_code);

-- Bildirishnoma o'qish
CREATE INDEX idx_notification_user_read ON notifications_notification (user_id, is_read);
```

---

## 6. MA'LUMOT HAJMI BAHOLASH

### 6.1. Bitta sayt uchun (oylik)

Taxminiy hisob-kitob (10,000 unique visitor/oy):

| Jadval | Yozuv | Hajm (taxmin) |
|--------|-------|---------------|
| Session | 30,000 (3 visit/visitor) | ~10 MB |
| PageView | 90,000 (3 page/session) | ~30 MB |
| Event | 50,000 | ~10 MB |
| **Jami** | | **~50 MB** |

### 6.2. Yillik

Bitta sayt uchun: ~600 MB
100 sayt uchun: ~60 GB

→ SQLite chegarasini oshirsa, PostgreSQL'ga o'tish kerak.

---

## 7. MA'LUMOTLARNI SAQLASH SIYOSATI

| Jadval | Saqlash muddati | Tozalash |
|--------|-----------------|----------|
| User | Cheksiz | Manuel |
| Site | Cheksiz | Foydalanuvchi o'chirsa |
| Session | 90 kun | Cron job (django-q2) |
| PageView | 90 kun | Cron job |
| Event | 90 kun | Cron job |
| Notification | 30 kun (o'qilgan) | Cron job |
| Report | 365 kun | Cron job |

---

## 8. MIGRATSIYALAR

Django migratsiyalar `python manage.py makemigrations` orqali avtomatik yaratiladi. Har bir o'zgarish alohida migratsiya fayli sifatida saqlanadi va versiyalanadi.

### 8.1. Migratsiyalarni qo'llash

```bash
# Lokal dev
python manage.py migrate

# Production
python manage.py migrate --noinput
```

### 8.2. Yangi migratsiya yaratish

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 9. SEED MA'LUMOTLAR

Demo ma'lumotlar `python manage.py loaddata fixtures/demo.json` orqali yuklanadi:

- 1 superuser (admin@example.com / admin)
- 2 oddiy foydalanuvchi
- 3 demo sayt (har biri uchun)
- 1000 sessiya, 3000 page view, 500 event
- Turli mamlakatlar va brauzerlar

---

## 10. BACKUP VA RECOVERY

### 10.1. SQLite

```bash
# Backup
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# Restore
cp backup_20260501.sqlite3 db.sqlite3
```

### 10.2. PostgreSQL

```bash
# Backup
pg_dump -U user veb_monitoring > backup.sql

# Restore
psql -U user veb_monitoring < backup.sql
```

---

## 11. KENGAYTIRISH IMKONIYATLARI

- **Partitioning:** PageView jadvalini oy bo'yicha partition'larga bo'lish (PostgreSQL)
- **Read replica:** Analytics so'rovlar uchun
- **Time-series DB:** TimescaleDB yoki ClickHouse (yuqori yuk)
- **Caching:** Materialized views (PostgreSQL)
