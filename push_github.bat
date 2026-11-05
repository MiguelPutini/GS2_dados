@echo off
chcp 65001 > nul
cls
echo ====================================================================
echo  Enviando arquivos para o GitHub: https://github.com/MiguelPutini/GS2_dados.git
echo ====================================================================
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ====================================================================
    echo  [SUCESSO] Todos os arquivos foram enviados para o GitHub!
    echo ====================================================================
) else (
    echo.
    echo [AVISO] Se uma janela do navegador abrir solicitando permissao do GitHub,
    echo         clique em 'Authorize' para autenticar sua conta.
)
echo.
pause
