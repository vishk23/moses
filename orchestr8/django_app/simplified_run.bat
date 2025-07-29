@echo off
cd /d %~dp0
echo Starting Server...
start "Server" cmd /k "call ../../.venv/Scripts/activate && waitress-serve --host=127.0.0.1 --port=8000 django_app.wsgi:application"
@REM echo Starting Scheduler...
@REM start "Scheduler" cmd /k "call ../../.venv/Scripts/activate && celery -A django_app beat --loglevel=info"
echo Starting Worker...
start "Worker" cmd /k "call ../../.venv/Scripts/activate && celery -A django_app worker --pool=solo --loglevel=info"
echo All services started. Feel free to close this window, but leave the others open.
pause
