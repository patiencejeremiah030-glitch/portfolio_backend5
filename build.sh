#!/usr/bin/env bash
# Render (and similar) build step: install deps, apply migrations, collect static assets.
set -o errexit
set -o pipefail

pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
