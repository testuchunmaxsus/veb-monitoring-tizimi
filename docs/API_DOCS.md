# API HUJJATLARI

## Veb-Monitoring Tizimi — REST API spetsifikatsiyasi

> Interaktiv hujjatlash: **Swagger UI** — http://localhost:8000/api/docs/
> ReDoc — http://localhost:8000/api/redoc/
> OpenAPI schema — http://localhost:8000/api/schema/

---

## 1. UMUMIY MA'LUMOTLAR

### 1.1. Asosiy URL

| Muhit | Base URL |
|-------|----------|
| Dev | `http://localhost:8000/api/v1` |
| Production | `https://veb-monitoring.example.com/api/v1` |

### 1.2. Format

- Request va response: **JSON** (application/json)
- Sana formati: **ISO 8601** (`2026-05-01T14:30:00Z`)
- Kodlash: **UTF-8**

### 1.3. Autentifikatsiya

JWT (JSON Web Token) Bearer header orqali:

```
Authorization: Bearer <access_token>
```

`/auth/*` va `/track/*` endpointlari ochiq (token kerak emas).

### 1.4. Status kodlar

| Kod | Ma'nosi |
|-----|---------|
| 200 OK | Muvaffaqiyatli so'rov |
| 201 Created | Resurs yaratildi |
| 204 No Content | Muvaffaqiyatli, javob yo'q |
| 400 Bad Request | Noto'g'ri ma'lumot |
| 401 Unauthorized | Token yo'q yoki noto'g'ri |
| 403 Forbidden | Ruxsat yo'q |
| 404 Not Found | Resurs topilmadi |
| 409 Conflict | Resurs allaqachon mavjud |
| 422 Unprocessable Entity | Validatsiya xatosi |
| 429 Too Many Requests | Rate limit |
| 500 Internal Server Error | Server xatosi |

### 1.5. Xatolik formati

```json
{
  "detail": "Xato xabari",
  "errors": {
    "email": ["Email noto'g'ri formatda"]
  }
}
```

### 1.6. Pagination formati

```json
{
  "count": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8,
  "next": "http://localhost:8000/api/v1/sites/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 2. AUTH (AUTENTIFIKATSIYA) — `/auth`

### 2.1. POST `/auth/register/`

Yangi foydalanuvchi ro'yxatdan o'tkazadi.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "kuchli-parol-123",
  "full_name": "Ismoilov Javohir"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Ismoilov Javohir",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1Qi...",
    "refresh": "eyJ0eXAiOiJKV1Qi..."
  }
}
```

---

### 2.2. POST `/auth/login/`

Tizimga kirish.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "kuchli-parol-123"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Ismoilov Javohir"
  }
}
```

---

### 2.3. POST `/auth/refresh/`

Access tokenni yangilash.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

---

### 2.4. GET `/auth/me/`

Joriy foydalanuvchi profilini qaytaradi.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Ismoilov Javohir",
  "date_joined": "2026-04-15T10:30:00Z"
}
```

---

### 2.5. POST `/auth/logout/`

Refresh tokenni blacklist qiladi.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**Response (204)**

---

## 3. SITES (SAYTLAR) — `/sites`

### 3.1. GET `/sites/`

Foydalanuvchining barcha saytlari.

**Query params:**
- `page` (int, default: 1)
- `page_size` (int, default: 20)
- `search` (string, optional)

**Response (200):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "Mening blogim",
      "domain": "blog.example.com",
      "api_key": "vmt_aBc1XYz2dEf3...",
      "is_active": true,
      "created_at": "2026-04-20T10:00:00Z"
    }
  ]
}
```

---

### 3.2. POST `/sites/`

Yangi sayt qo'shadi.

**Request:**
```json
{
  "name": "Mening blogim",
  "domain": "blog.example.com"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Mening blogim",
  "domain": "blog.example.com",
  "api_key": "vmt_aBc1XYz2dEf3GhI4jKl5mNo6pQrStUvW",
  "is_active": true,
  "created_at": "2026-05-01T12:00:00Z"
}
```

---

### 3.3. GET `/sites/{id}/`

Bitta sayt tafsilotlari.

**Response (200):** Site obyekti.

---

### 3.4. PATCH `/sites/{id}/`

Sayt sozlamalarini yangilash.

**Request:**
```json
{
  "name": "Yangi nom",
  "is_active": false
}
```

**Response (200):** Yangilangan Site obyekti.

---

### 3.5. DELETE `/sites/{id}/`

Saytni va barcha statistikasini o'chiradi.

**Response (204)**

---

### 3.6. POST `/sites/{id}/regenerate-api-key/`

API kalitni yangilaydi.

**Response (200):**
```json
{
  "api_key": "vmt_yangi_kalit..."
}
```

---

## 4. TRACKING (KUZATUV) — `/track`

> Ushbu endpointlar **public** (token kerak emas), API kalit asosida ishlaydi.

### 4.1. POST `/track/pageview/`

Sahifa ko'rishini qayd etadi.

**Request:**
```json
{
  "api_key": "vmt_aBc1XYz2dEf3...",
  "session_uid": "uuid-v4-generated-by-tracker",
  "url": "https://example.com/page",
  "title": "Sahifa sarlavhasi",
  "referrer": "https://google.com",
  "load_time_ms": 1250,
  "lcp_ms": 1800,
  "fcp_ms": 900,
  "ttfb_ms": 200
}
```

**Response (201):**
```json
{
  "ok": true
}
```

---

### 4.2. POST `/track/event/`

Custom event qayd etadi.

**Request:**
```json
{
  "api_key": "vmt_aBc1XYz2dEf3...",
  "session_uid": "uuid-v4-...",
  "type": "click",
  "target": "button#cta",
  "metadata": {
    "label": "Asosiy harakat tugmasi"
  }
}
```

**Response (201):** `{"ok": true}`

---

### 4.3. POST `/track/session/end/`

Sessiya tugashini bildiradi (sendBeacon target).

**Request:**
```json
{
  "api_key": "vmt_aBc1XYz2dEf3...",
  "session_uid": "uuid-v4-...",
  "duration_sec": 245
}
```

**Response (200):** `{"ok": true}`

---

## 5. ANALYTICS (TAHLIL) — `/analytics`

Barcha endpointlar token va `?site_id=` parametrini talab qiladi.

### 5.1. GET `/analytics/overview/`

Umumiy ko'rsatkichlar.

**Query params:**
- `site_id` (int, **majburiy**)
- `from` (date, default: 7 kun oldin)
- `to` (date, default: bugun)

**Response (200):**
```json
{
  "total_pageviews": 12500,
  "unique_visitors": 4300,
  "total_sessions": 5200,
  "bounce_rate": 0.42,
  "avg_session_duration_sec": 180,
  "comparison": {
    "pageviews_delta_pct": 12.5,
    "visitors_delta_pct": 8.3
  }
}
```

---

### 5.2. GET `/analytics/timeseries/`

Vaqt bo'yicha grafik ma'lumotlari.

**Query params:**
- `site_id` (int)
- `from`, `to` (date)
- `interval` (string: `hour`, `day`, default: `day`)
- `metric` (string: `pageviews`, `visitors`, `sessions`)

**Response (200):**
```json
{
  "interval": "day",
  "metric": "pageviews",
  "data": [
    {"timestamp": "2026-04-25T00:00:00Z", "value": 1500},
    {"timestamp": "2026-04-26T00:00:00Z", "value": 1700}
  ]
}
```

---

### 5.3. GET `/analytics/top-pages/`

Eng mashhur sahifalar.

**Query params:**
- `site_id`, `from`, `to`
- `limit` (int, default: 10)

**Response (200):**
```json
{
  "results": [
    {"url": "/", "title": "Bosh sahifa", "views": 5200, "unique_visitors": 3100},
    {"url": "/blog", "title": "Blog", "views": 2300, "unique_visitors": 1800}
  ]
}
```

---

### 5.4. GET `/analytics/top-referrers/`

Eng mashhur manbalar.

**Response (200):**
```json
{
  "results": [
    {"referrer": "google.com", "visits": 3500},
    {"referrer": "direct", "visits": 2100}
  ]
}
```

---

### 5.5. GET `/analytics/devices/`

Qurilma turlari.

**Response (200):**
```json
{
  "by_device": {"desktop": 60, "mobile": 35, "tablet": 5},
  "by_browser": {"Chrome": 65, "Firefox": 18, "Safari": 12},
  "by_os": {"Windows": 50, "Android": 25, "iOS": 15}
}
```

---

### 5.6. GET `/analytics/geo/`

Geografik bo'linish.

**Response (200):**
```json
{
  "by_country": [
    {"code": "UZ", "name": "Uzbekistan", "visits": 4200},
    {"code": "RU", "name": "Russia", "visits": 800}
  ],
  "by_city": [
    {"name": "Toshkent", "country": "UZ", "visits": 2500}
  ]
}
```

---

### 5.7. GET `/analytics/heatmap/`

Klik heatmap.

**Query params:**
- `site_id`, `from`, `to`
- `url` (string)

**Response (200):**
```json
{
  "url": "/landing",
  "viewport_width": 1920,
  "viewport_height": 1080,
  "points": [
    {"x": 320, "y": 450, "count": 25},
    {"x": 480, "y": 600, "count": 18}
  ]
}
```

---

### 5.8. GET `/analytics/funnel/`

Funnel analiz.

**Query params:**
- `site_id`
- `steps` (string, comma-separated URLs)

**Response (200):**
```json
{
  "steps": [
    {"url": "/", "count": 10000, "drop_pct": 0},
    {"url": "/product", "count": 6500, "drop_pct": 35},
    {"url": "/cart", "count": 2000, "drop_pct": 69},
    {"url": "/checkout", "count": 1200, "drop_pct": 40}
  ]
}
```

---

## 6. REPORTS (HISOBOTLAR) — `/reports`

### 6.1. POST `/reports/generate/`

Hisobot generatsiyasini boshlaydi (asinxron).

**Request:**
```json
{
  "site_id": 1,
  "format": "pdf",
  "date_from": "2026-04-01",
  "date_to": "2026-04-30"
}
```

**Response (202):**
```json
{
  "id": 15,
  "status": "pending",
  "format": "pdf"
}
```

---

### 6.2. GET `/reports/`

Hisobotlar tarixi.

**Response (200):** Pagination + ro'yxat.

---

### 6.3. GET `/reports/{id}/download/`

Hisobotni yuklab olish.

**Response (200):** Fayl (Content-Type: application/pdf yoki text/csv).

---

## 7. NOTIFICATIONS (BILDIRISHNOMALAR) — `/notifications`

### 7.1. GET `/notifications/`

Foydalanuvchi bildirishnomalari.

**Query params:**
- `unread_only` (boolean)

**Response (200):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "type": "anomaly",
      "title": "Trafik anomaliyasi",
      "message": "Soat 14:00'da trafik 200% oshib ketdi",
      "is_read": false,
      "created_at": "2026-05-01T14:05:00Z"
    }
  ]
}
```

---

### 7.2. POST `/notifications/{id}/mark-read/`

Bildirishnomani o'qildi deb belgilash.

**Response (204)**

---

### 7.3. POST `/notifications/mark-all-read/`

Barchasini o'qildi deb belgilash.

**Response (204)**

---

## 8. WEBSOCKET — `/ws`

### 8.1. `/ws/site/{id}/`

Sayt uchun real-time hodisalar oqimi.

**Query params:**
- `token` (string, JWT access token)

**Server → Client xabarlari:**

```json
{
  "type": "pageview",
  "data": {
    "url": "/blog",
    "country": "UZ",
    "browser": "Chrome",
    "timestamp": "2026-05-01T14:30:00Z"
  }
}
```

```json
{
  "type": "online_count",
  "data": {"count": 25}
}
```

---

## 9. RATE LIMITING

| Guruh | Cheklov |
|-------|---------|
| Anon foydalanuvchi | 100 /min |
| Login foydalanuvchi | 1000 /min |
| Tracking endpoints | 10 000 /min per API key |

Limit oshganda javob:
```json
{
  "detail": "So'rovlar soni cheklangan. Birozdan keyin urinib ko'ring."
}
```

Status: `429 Too Many Requests`

---

## 10. SWAGGER UI

Interaktiv hujjatlash va endpointlarni sinab ko'rish uchun:

**http://localhost:8000/api/docs/**

Bu yerda:
- Barcha endpointlar avtomatik dokumentlangan
- "Authorize" tugmasi orqali JWT token kiritish mumkin
- Har bir endpoint uchun "Try it out" funksiyasi
- Request/Response schema'lari ko'rinadi

---

## 11. POSTMAN COLLECTION

OpenAPI schema'ni Postman'ga import qilish uchun:

```
http://localhost:8000/api/schema/
```

Postman'da: `Import → Link → URL`
