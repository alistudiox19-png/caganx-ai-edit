@echo off
chcp 65001 > nul
title caganx AI edit - Ozel Admin Masaustu Uygulamasi
color 0A

echo ========================================================
echo  🛡️ caganx AI edit - Masaustu Admin Uygulamasi Baslatiliyor...
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/1] Uygulama Penceresi Aciliyor...
python admin_app.py

exit
