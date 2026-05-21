@echo off
chcp 65001 >nul
echo ========================================
echo  Veb-Monitoring loyihasi setup
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Backend setup
call backend\setup.bat
if errorlevel 1 goto :error

echo.
echo [2/3] Frontend dependencies o'rnatilmoqda...
cd frontend
call npm install
if errorlevel 1 goto :error
if not exist ".env" copy .env.example .env >nul
cd ..

echo.
echo [3/3] Tracker dependencies o'rnatilmoqda va build...
cd tracker
call npm install
if errorlevel 1 goto :error
call npm run build
cd ..

echo.
echo ========================================
echo  Setup muvaffaqiyatli yakunlandi!
echo ========================================
echo.
echo Loyihani ishga tushirish uchun:
echo    start.bat
echo.
echo Yoki demo ma'lumotlar bilan:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py shell ^< scripts\seed.py
echo    cd ..
echo    start.bat
echo.
echo Demo login: demo@example.com / demo1234
echo.
pause
exit /b 0

:error
echo.
echo XATO YUZ BERDI! Yuqoridagi xabarlarni o'qing.
pause
exit /b 1
