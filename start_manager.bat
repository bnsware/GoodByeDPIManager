@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 🚀 GoodBye DPI Manager başlatılıyor...
echo.

REM Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ HATA: Python bulunamadı!
    echo Python'u https://python.org adresinden indirip yüklemelisiniz.
    pause
    exit /b 1
)

REM Gerekli kütüphaneleri kontrol et ve yükle
echo 📦 Gerekli kütüphaneler kontrol ediliyor...
pip show psutil >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 psutil kütüphanesi yükleniyor...
    pip install psutil
)

pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 requests kütüphanesi yükleniyor...
    pip install requests
)

echo.
echo 🎯 GoodBye DPI Manager başlatılıyor...
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
python goodbyedpi_manager.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ HATA: Uygulama çalıştırılırken bir hata oluştu!
    echo ⚠️ Yönetici yetkileri ile çalıştırmayı deneyin.
    echo 📧 Sorun devam ederse: https://github.com/ByNoSoftware
    pause
)