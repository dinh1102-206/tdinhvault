@echo off
title FORGE TOOL DA CHUC NANG
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 pause
