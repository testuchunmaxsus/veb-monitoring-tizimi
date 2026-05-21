@echo off
chcp 65001 >nul
echo ========================================
echo  Backend setup boshlandi
echo ========================================
cd /d "%~dp0"

if not exist "venv" (
    echo [1/5] Virtual environment yaratilmoqda...
    python -m venv venv
) else (
    echo [1/5] Virtual environment mavjud
)

echo [2/5] Dependencies o'rnatilmoqda (~3-5 daqiqa)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if not exist ".env" (
    echo [3/5] .env fayli yaratilmoqda...
    copy .env.example .env >nul
)

echo [4/5] Migratsiyalar qo'llanmoqda...
python manage.py migrate

echo [5/5] Tayyor! Endi superuser yarating:
echo    venv\Scripts\activate
echo    python manage.py createsuperuser
echo.
echo Demo ma'lumotlar uchun:
echo    python manage.py shell ^< scripts\seed.py
echo.
pause
