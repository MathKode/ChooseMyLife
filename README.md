# ChooseMyLife
It's more than a simple local-password manager : yep, it's here to make easier the internet Anonymat !

## Installation 

First Step : Get the script on your laptop !
```
git clone https://github.com/MathKode/ChooseMyLife/
```
Or Download the zip here : [Zip_File](https://github.com/MathKode/ChooseMyLife/archive/refs/heads/main.zip)


Second Step : Install the python lib.

```
pip install django
cd ChooseMyLife\ChooseMyLife
@echo off
echo cd %cd% > start_up.bat
echo python manage.py runserver >> start_up.bat

:: Tunr into ADMIN (to copy the start_up.bat file)
:: from https://stackoverflow.com/questions/11525056/how-to-create-a-batch-file-to-run-cmd-as-administrator
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
set params = %*:"="
echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"

copy "start_up.bat"  "%ProgramData%\Microsoft\Windows\Start Menu\Programs\choosemylife.bat"
exit
@echo on
python manage.py runserver
```
