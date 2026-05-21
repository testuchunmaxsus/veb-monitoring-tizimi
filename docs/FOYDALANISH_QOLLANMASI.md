# FOYDALANISH QO'LLANMASI

## Veb-Monitoring Tizimi — O'rnatish va foydalanish

---

## 1. TIZIM TALABLARI

### 1.1. Apparat talablari

| Komponent | Minimal | Tavsiya etiladigan |
|-----------|---------|--------------------|
| RAM | 4 GB | 8 GB+ |
| Disk | 2 GB bo'sh joy | 5 GB+ |
| CPU | 2 yadro | 4 yadro+ |

### 1.2. Operatsion tizimlar

- Windows 10/11
- macOS 12+
- Ubuntu 20.04+
- Boshqa Linux distrolari

### 1.3. Dasturiy ta'minot

| Dastur | Versiya | Yuklab olish |
|--------|---------|---------------|
| Python | 3.11 yoki yangiroq | https://python.org/downloads/ |
| Node.js | 20 LTS yoki yangiroq | https://nodejs.org/ |
| Git (ixtiyoriy) | 2.40+ | https://git-scm.com/ |

---

## 2. O'RNATISH

### 2.1. Loyihani yuklab olish

#### Variant A: ZIP fayl orqali

1. Loyiha arxivini oching (`Javohir.zip`)
2. Istalgan papkaga distrobyutsiya qiling (masalan, `D:\Ulugbek\2025-2026\Kur ishi\Javohir`)

#### Variant B: Git orqali

```bash
git clone <repository-url>
cd Javohir
```

### 2.2. Backend o'rnatish

#### 1-qadam: Virtual environment yaratish

**Windows:**
```batch
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2-qadam: Dependencies o'rnatish

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> Bu ~3-5 daqiqa vaqt oladi.

#### 3-qadam: Muhit o'zgaruvchilarini sozlash

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

`.env` faylini oching va kerak bo'lsa o'zgartiring (default qiymatlar lokal dev uchun yetarli).

#### 4-qadam: Database migratsiyalarini qo'llash

```bash
python manage.py migrate
```

> SQLite ishlatilsa, `db.sqlite3` fayli avtomatik yaratiladi.

#### 5-qadam: Superuser (administrator) yaratish

```bash
python manage.py createsuperuser
```

Email va parolni kiriting (admin paneliga kirish uchun).

#### 6-qadam (ixtiyoriy): Demo ma'lumotlarni yuklash

```bash
python manage.py loaddata fixtures/demo.json
```

---

### 2.3. Frontend o'rnatish

```bash
cd frontend
npm install
```

> Bu ~2-3 daqiqa vaqt oladi.

`.env` faylni yarating:

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

---

### 2.4. Tracker build qilish

```bash
cd tracker
npm install
npm run build
```

Natija: `tracker/dist/tracker.min.js` (~5 KB).

---

## 3. ISHGA TUSHIRISH

### 3.1. Tezkor usul (Windows)

Loyiha ildizidan:

```batch
start.bat
```

Bu skript backend va frontend'ni bir vaqtda ishga tushiradi.

### 3.2. Tezkor usul (Linux/macOS)

```bash
chmod +x start.sh
./start.sh
```

### 3.3. Qo'lda ishga tushirish

#### Backend (Terminal 1):

**Windows:**
```batch
cd backend
venv\Scripts\activate
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

#### Frontend (Terminal 2):

```bash
cd frontend
npm run dev
```

#### Background worker (Terminal 3, ixtiyoriy):

```bash
cd backend
venv\Scripts\activate    # yoki source venv/bin/activate
python manage.py qcluster
```

> Bildirishnomalar va anomaliya detection uchun kerak.

### 3.4. Ochiq portlar

| Xizmat | URL |
|--------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/v1/ |
| API Docs (Swagger) | http://localhost:8000/api/docs/ |
| API Docs (ReDoc) | http://localhost:8000/api/redoc/ |
| Admin panel | http://localhost:8000/admin/ |

---

## 4. ASOSIY FOYDALANISH

### 4.1. Birinchi marta foydalanish

#### 1. Ro'yxatdan o'ting

1. Brauzerni oching: http://localhost:5173
2. "Ro'yxatdan o'tish" tugmasini bosing
3. Email, parol va to'liq ismni kiriting
4. "Ro'yxatdan o'tish" tugmasini bosing

#### 2. Sayt qo'shing

1. Dashboardda "Sayt qo'shish" tugmasini bosing
2. Sayt nomi va domenni kiriting
3. "Saqlash" tugmasini bosing
4. Tracker JavaScript kod ko'rsatiladi

#### 3. Tracker'ni saytingizga qo'shing

Sizning saytingizning HTML'iga `<head>` ichiga quyidagi kodni qo'ying:

```html
<script
  async
  src="http://localhost:8000/static/tracker.min.js"
  data-api-key="vmt_sizning_kalitingiz"
  data-endpoint="http://localhost:8000/api/v1/track">
</script>
```

#### 4. Statistikani ko'ring

1. Saytingizga kiring (sahifaga tashrif buyuring)
2. Dashboardni yangilang
3. Tashriflar, sessiyalar va qurilmalar haqida ma'lumot ko'rinadi

### 4.2. Test qilish

`tracker/examples/demo.html` faylini brauzerda oching:
- Sahifa ko'rishi avtomatik qayd etiladi
- "Test tugma"ga bosing — klik event yoziladi
- Dashboard'ga qaytib, real vaqt rejimida o'zgarishlarni kuzating

---

## 5. ADMIN PANELDAN FOYDALANISH

### 5.1. Kirish

1. http://localhost:8000/admin/ ga kiring
2. Superuser email va parolni kiriting

### 5.2. Mavjud bo'limlar

- **Foydalanuvchilar** — barcha ro'yxatdan o'tganlar
- **Saytlar** — barcha qo'shilgan saytlar
- **Sessiyalar** — har bir tashrif buyuruvchi sessiyasi
- **Sahifa ko'rishlari** — har bir sahifa visit
- **Hodisalar** — kliklar, formlar
- **Bildirishnomalar** — tizim xabarlari

---

## 6. DASHBOARD FUNKSIYALARI

### 6.1. Asosiy dashboard

- **Umumiy ko'rsatkichlar** — jami ko'rishlar, unikal tashrif buyuruvchilar, sessiyalar, bounce rate
- **Vaqt grafigi** — kun yoki soat bo'yicha trafik
- **Eng mashhur sahifalar** — top 10 sahifa
- **Manbalar** — qaysi saytlardan keldi

### 6.2. Sayt tafsilotlari

Tabs:
- **Umumiy** — barcha statistika
- **Sahifalar** — sahifalar bo'yicha tahlil
- **Xulq-atvor** — heatmap, funnel
- **Real vaqt** — jonli oqim

### 6.3. Filtrlar

- **Sana oralig'i** — bugun, 7 kun, 30 kun, custom
- **Sayt** — bir nechta sayt orasidan tanlash
- **URL** — aniq sahifa bo'yicha filtrlash

---

## 7. HISOBOTLAR

### 7.1. PDF hisobot olish

1. "Hisobotlar" sahifasini oching
2. Sayt va sana oralig'ini tanlang
3. "PDF" formatini tanlang
4. "Yaratish" tugmasini bosing
5. Tayyor bo'lgach, "Yuklab olish" tugmasini bosing

### 7.2. CSV eksport

Xom ma'lumotlarni Excel yoki Google Sheets'da tahlil qilish uchun:
1. "CSV" formatini tanlang
2. Yaratish va yuklab olish

---

## 8. MUAMMOLARNI HAL QILISH

### 8.1. Backend ishga tushmasdi

**Xato:** `ModuleNotFoundError: No module named 'django'`

**Yechim:** Virtual environment faollashtirilganligini tekshiring:
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 8.2. Migratsiyalar xatosi

**Xato:** `django.db.utils.OperationalError: no such table`

**Yechim:**
```bash
python manage.py migrate
```

### 8.3. Frontend port band

**Xato:** `Port 5173 is already in use`

**Yechim:** `frontend/vite.config.ts` faylida `port` ni o'zgartiring yoki:
```bash
# Boshqa port'da ishga tushiring
npm run dev -- --port 5174
```

### 8.4. Tracker ishlamayapti

**Tekshiring:**
1. Brauzer DevTools → Network tab — `/track/pageview` so'rovi yuborilmoqdami?
2. Console'da xatolar yo'qmi?
3. API kalit to'g'ri ko'chirilganmi?
4. Backend ishlayaptimi (http://localhost:8000)?

### 8.5. CORS xatolari

**Xato:** `Access to XMLHttpRequest blocked by CORS`

**Yechim:** `backend/.env` faylida `CORS_ALLOWED_ORIGINS` ga o'z domeningizni qo'shing:
```
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://your-site.com
```

### 8.6. WebSocket ulana olmayapti

**Yechim:**
1. Daphne ishlaydimi tekshiring (runserver emas, daphne kerak)
2. `/ws/site/{id}/?token=...` to'g'ri formatdami
3. Brauzer console'da error nima

---

## 9. PRODUCTION'DA ISHGA TUSHIRISH

### 9.1. PostgreSQL'ga o'tish

`.env` faylida:
```
DATABASE_URL=postgres://user:password@localhost:5432/veb_monitoring
```

Migratsiyalarni qayta qo'llang:
```bash
python manage.py migrate
```

### 9.2. Redis qo'shish (Channels uchun)

```
REDIS_URL=redis://localhost:6379/0
```

### 9.3. Frontend production build

```bash
cd frontend
npm run build
# Natija: dist/
```

`dist/` papkasini nginx orqali serve qiling.

### 9.4. Daphne'ni systemd orqali ishga tushirish (Linux)

`/etc/systemd/system/veb-monitoring.service`:

```ini
[Unit]
Description=Veb-Monitoring Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/veb-monitoring/backend
Environment="DJANGO_SETTINGS_MODULE=config.settings.prod"
ExecStart=/var/www/veb-monitoring/backend/venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable veb-monitoring
sudo systemctl start veb-monitoring
```

---

## 10. YANGILANISH (UPDATE)

```bash
# Backend
cd backend
venv\Scripts\activate
git pull   # yoki yangi fayllarni nusxa ko'chiring
pip install -r requirements.txt
python manage.py migrate

# Frontend
cd frontend
npm install
npm run build
```

---

## 11. KONTAKT

Savollar yoki muammolar bo'yicha:

- **Talaba:** Ismoilov Javohir Ulug'bek o'g'li
- **Email:** geminiuchunmaxsus@gmail.com
- **Rahbar:** Tojimamatov Israil Nurmamatovich

---

## 12. LITSENZIYA

O'quv maqsadlarida ishlab chiqilgan. FarDU 2025-2026 o'quv yili kurs ishi.
