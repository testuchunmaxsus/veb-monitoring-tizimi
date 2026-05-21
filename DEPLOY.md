# Deploy qo'llanmasi

## Arxitektura

```
[Vercel - Frontend]  <-->  [Railway - Backend + PostgreSQL + Redis]
```

---

## 1. Backend - Railway

### 1.1 Railway'da yangi loyiha yaratish

1. https://railway.app ga kiring
2. **New Project** → **Deploy from GitHub repo**
3. GitHub repositoriyani ulang
4. **Root Directory** ni `backend` ga o'zgartiring

### 1.2 PostgreSQL qo'shish

1. Railway dashboard → **+ New** → **Database** → **PostgreSQL**
2. `DATABASE_URL` avtomatik o'rnatiladi

### 1.3 Redis qo'shish (WebSocket uchun, ixtiyoriy)

1. Railway dashboard → **+ New** → **Database** → **Redis**
2. `REDIS_URL` avtomatik o'rnatiladi

### 1.4 Environment variables o'rnatish

Railway → Backend service → **Variables** bo'limiga quyidagilarni qo'shing:

```
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=<uzun-random-string-generatsiya-qiling>
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
FRONTEND_URL=https://your-frontend.vercel.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
```

> `SECRET_KEY` uchun: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 1.5 Deploy tekshirish

Deploy tugagandan so'ng:
- Health check: `https://your-app.up.railway.app/api/v1/health/`
- Admin panel: `https://your-app.up.railway.app/admin/`
- Swagger: `https://your-app.up.railway.app/api/docs/`

### 1.6 Superuser yaratish

Railway → Backend service → **Settings** → **Run Command** (bir martalik):
```bash
python manage.py createsuperuser --email admin@example.com --noinput
```

Yoki Railway CLI:
```bash
railway run python manage.py createsuperuser
```

---

## 2. Frontend - Vercel

### 2.1 Vercel'da deploy qilish

1. https://vercel.com ga kiring
2. **New Project** → GitHub repo tanlang
3. **Root Directory** ni `frontend` ga o'zgartiring
4. Framework: **Vite** (avtomatik aniqlanadi)

### 2.2 Environment variables o'rnatish

Vercel → Project → **Settings** → **Environment Variables**:

```
VITE_API_URL=https://your-backend.up.railway.app/api/v1
VITE_WS_URL=wss://your-backend.up.railway.app/ws
```

### 2.3 Deploy tekshirish

- Frontend: `https://your-frontend.vercel.app`
- Login sahifaga o'tishi kerak

---

## 3. Deploy ketma-ketligi

1. **Avval** Railway'da backend deploy qiling
2. Backend URL'ni oling (masalan: `https://veb-monitoring-backend.up.railway.app`)
3. Railway'da `CORS_ALLOWED_ORIGINS` va `FRONTEND_URL` ni yangilang
4. Vercel'da frontend deploy qiling, `VITE_API_URL` ni backend URL bilan to'ldiring
5. Frontend URL'ni oling va Railway'dagi `CORS_ALLOWED_ORIGINS`ga qo'shing

---

## 4. Seed data (ixtiyoriy)

```bash
railway run python manage.py seed
```

---

## 5. Xatolarni bartaraf etish

| Muammo | Yechim |
|--------|--------|
| 500 error | Railway Logs tekshiring, `SECRET_KEY` o'rnatilganmi? |
| CORS error | `CORS_ALLOWED_ORIGINS` to'g'ri frontend URL bormi? |
| Static 404 | `collectstatic` ishlayaptimi? Whitenoise middleware bormi? |
| DB error | `DATABASE_URL` PostgreSQL formatda bormi? |
| WebSocket fail | `REDIS_URL` o'rnatilganmi? `wss://` ishlatilayaptimi? |
