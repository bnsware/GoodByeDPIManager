@ECHO OFF
cd /d "%~dp0"
python gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Hata olustu! gui_hata.txt dosyasini kontrol edin.
    pause
)
