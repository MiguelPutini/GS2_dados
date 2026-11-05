@echo off
chcp 65001 > nul
cls
echo ====================================================================
echo  Executando Demonstracao Pratica Guiada (DSA)
echo  Global Solution 2026.2 - Data Structures and Algorithms
echo ====================================================================

where python >nul 2>nul
if %errorlevel% equ 0 (
    python demo.py
) else (
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" demo.py
    ) else (
        echo [ERRO] Python 3 nao encontrado no PATH do sistema.
    )
)
pause

