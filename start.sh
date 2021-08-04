#!/usr/bin/env bash

python3 manage.py collectstatic --clear --noinput
python3 manage.py migrate

gunicorn Billing.wsgi:application -t 600 -b 0.0.0.0:8000