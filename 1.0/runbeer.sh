#!/bin/bash
source ./venv/bin/activate
gunicorn -D --workers=3 -n beervintory -u www-data -g www-data -b 127.0.0.1:8000 -p /var/www/beervintory/run.pid run:app
