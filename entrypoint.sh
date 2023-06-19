#!/bin/bash

# Apply database migrations
poetry run python manage.py migrate
# Collect static files
poetry run python manage.py collectstatic --noinput

# Prepare gunicorn log files
mkdir -p /task_manager/deployment/logs/gunicorn/

touch /task_manager/deployment/logs/gunicorn/access.log
touch /task_manager/deployment/logs/gunicorn/error.log
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn task_manager.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --access-logfile=/task_manager/deployment/logs/gunicorn/access.log \
    --error-logfile=/task_manager/deployment/logs/gunicorn/error.log \
    --capture-output \
    "$@"
