@echo off

CALL "%~dp0env\Scripts\activate" || EXIT /B 1
python manage.py runserver 




