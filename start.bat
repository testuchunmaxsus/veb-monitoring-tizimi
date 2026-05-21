@echo off
chcp 65001 >nul
echo ========================================
echo  Veb-Monitoring Tizimi - Ishga tushish
echo ========================================
echo.

cd /d "%~dp0"

if not exist "backend\venv" (
    echo [XATO] Backend virtual environment topilmadi.
    echo Iltimos avval quyidagi buyruqlarni bajaring:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo   python manage.py migrate
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo [XATO] Frontend dependencies topilmadi.
    echo Iltimos avval quyidagi buyruqni bajaring:
    echo   cd frontend
    echo   npm install
    pause
    exit /b 1
)

echo [1/2] Backend ishga tushirilmoqda (port 8000)...
start "Backend - Django Channels" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && daphne -b 0.0.0.0 -p 8000 config.asgi:application"

timeout /t 3 /nobreak >nul

echo [2/2] Frontend ishga tushirilmoqda (port 5173)...
start "Frontend - Vite" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo  Loyiha ishga tushirildi!
echo ========================================
echo  Backend API:    http://localhost:8000
echo  API Docs:       http://localhost:8000/api/docs/
echo  Admin panel:    http://localhost:8000/admin/
echo  Frontend:       http://localhost:5173
echo ========================================
echo.
echo To'xtatish uchun ikkala terminal oynalarini yoping.
pause
