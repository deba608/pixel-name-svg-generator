@echo off
set /p NAME=Name: 
set /p SUBTITLE=Subtitle: 
if "%SUBTITLE%"=="" set SUBTITLE=AI ENGINEER ^| DEVELOPER
python "%~dp0generate_pixel_svg.py" --name "%NAME%" --subtitle "%SUBTITLE%"
pause
