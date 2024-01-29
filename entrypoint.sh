#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

gunicorn nipps_hms.wsgi:application --bind 0.0.0.0:8000 --timeout 120
