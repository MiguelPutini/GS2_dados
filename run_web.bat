@echo off
chcp 65001 > nul
cls
echo ====================================================================
echo  Iniciando Portal Web Citizen Assist AI (Localhost:8080)
echo  Global Solution 2026.2 - Data Structures and Algorithms
echo ====================================================================

start http://localhost:8080

where python >nul 2>nul
if %errorlevel% equ 0 (
    python web_app.py
) else (
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" web_app.py
    ) else (
        echo [ERRO] Python 3 nao encontrado no PATH do sistema.
        pause
    )
)
pause

