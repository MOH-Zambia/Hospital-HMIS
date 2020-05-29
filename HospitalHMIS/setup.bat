@echo off

CALL "%~dp0env\Scripts\activate"

CALL pip install -r "%~dp0requirements.txt"

REM CALL python manage.py makemigrations
REM CALL python manage.py migrate

REM CALL python manage.py seed

PAUSE