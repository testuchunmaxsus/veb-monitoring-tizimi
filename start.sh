#!/usr/bin/env bash
set -e

echo "========================================"
echo " Veb-Monitoring Tizimi - Ishga tushish"
echo "========================================"

cd "$(dirname "$0")"

if [ ! -d "backend/venv" ]; then
  echo "[XATO] Backend virtual environment topilmadi."
  echo "Iltimos avval bajaring:"
  echo "  cd backend && python3 -m venv venv && source venv/bin/activate"
  echo "  pip install -r requirements.txt && python manage.py migrate"
  exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
  echo "[XATO] Frontend dependencies topilmadi."
  echo "Iltimos avval bajaring: cd frontend && npm install"
  exit 1
fi

cleanup() {
  echo ""
  echo "To'xtatilmoqda..."
  kill 0
}
trap cleanup EXIT INT TERM

echo "[1/2] Backend ishga tushirilmoqda (port 8000)..."
(cd backend && source venv/bin/activate && daphne -b 0.0.0.0 -p 8000 config.asgi:application) &

sleep 2

echo "[2/2] Frontend ishga tushirilmoqda (port 5173)..."
(cd frontend && npm run dev) &

echo ""
echo "========================================"
echo " Loyiha ishga tushirildi!"
echo "========================================"
echo " Backend API:    http://localhost:8000"
echo " API Docs:       http://localhost:8000/api/docs/"
echo " Admin panel:    http://localhost:8000/admin/"
echo " Frontend:       http://localhost:5173"
echo "========================================"
echo "To'xtatish uchun Ctrl+C bosing."

wait
