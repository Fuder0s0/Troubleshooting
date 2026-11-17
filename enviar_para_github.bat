@echo off
title Enviar Projeto para o GitHub - MPPE
echo ========================================================
echo   Enviando Troubleshooting SIMP-PE para o GitHub
echo ========================================================
echo.
echo Repositorio de destino: https://github.com/Fuder0s0/Troubleshooting.git
echo.
echo Se uma janela de login do GitHub aparecer no seu navegador,
echo basta clicar em "Authorize GitCredentialManager" com sua conta.
echo.
git push -u origin main --tags
echo.
if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo   PROJETO PUBLICADO COM SUCESSO NO GITHUB!
    echo ========================================================
) else (
    echo Ocorreu um erro no envio. Verifique as mensagens acima.
)
echo.
pause
