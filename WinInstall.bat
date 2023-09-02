@echo off
Windows\python.exe -m venv .venv/ChooseMyLife
.venv\ChooseMyLife\Scripts\activate.bat
pip install django

set /P id=Do you want start service at every start-up [Y/N] : 
IF "%id%"=="Y" (
  copy "Windows\start_server.bat"  "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\start_server.bat"
)

