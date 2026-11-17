@echo off
title Extrator de Mensagens WhatsApp SIMP - MPPE
echo ========================================================
echo   Iniciando Extrator Automatizado de Grupos do SIMP
echo ========================================================
echo.
echo Uma janela do Google Chrome sera aberta em web.whatsapp.com.
echo Se necessario, aponte a camera do seu celular para o QR Code.
echo Apos conectar, o sistema fara a busca e extracao de todos
echo os grupos que contenham "SIMP".
echo.
python "%~dp0scripts\scrape_whatsapp_simp.py"
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
