@echo off
chcp 65001 > nul
cls
echo ====================================================================
echo  Executando Suite de Testes Automatizados (unittest)
echo  Global Solution 2026.2 - Data Structures and Algorithms
echo ====================================================================

where python >nul 2>nul
if %errorlevel% equ 0 (
    python -m unittest discover -s testes -v
) else (
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" -m unittest discover -s testes -v
    ) else (
        echo [ERRO] Python 3 nao encontrado no PATH do sistema.
    )
)
pause

