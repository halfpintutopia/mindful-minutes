#!/usr/bin/env bash

set -o errexit  # exit on error

cd app
pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
