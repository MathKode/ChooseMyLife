# ChooseMyLife
It's more than a simple local-password manager : yep, it's here to make easier the internet Anonymat !

## Installation 

First Step : Get the script on your laptop !
```
git clone https://github.com/MathKode/ChooseMyLife/
```
Or Download the zip here : [Zip_File](https://github.com/MathKode/ChooseMyLife/archive/refs/heads/main.zip)


### Windows

First configure the start up file
```
pip install django
cd ChooseMyLife\ChooseMyLife
@echo off
echo cd %cd% > start_up.bat
echo python manage.py runserver >> start_up.bat
@echo on

```
Then execute ``start_up.bat`` wherever on your laptop : it will launch the script !
