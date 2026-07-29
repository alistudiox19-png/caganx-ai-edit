@echo off
chcp 65001 > nul
title caganx AI edit - Ozel Admin Kontrol Paneli Baslatici
color 0A

echo ========================================================
echo  🛡️ caganx AI edit - Ozel Admin Panel Baslatiliyor...
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/2] Arka Plan Admin Sunucusu Kontrol Ediliyor...
python -m pip install flask flask-cors psutil sqlite3 > nul 2>&1

echo [2/2] Sunucu Port 9090 Uzerinde Baslatiliyor...
start /b python admin_server.py > nul 2>&1

timeout /t 2 > nul

echo.
echo ========================================================
echo  🚀 ADMIN PANEL BASARIYLA ACILDI!
echo  🌐 Adres: http://localhost:9090
echo ========================================================
echo.

start http://localhost:9090

exit
