#!/bin/sh
# Commands for Starting Web Server/Injecting faust

python manage.py migrate &&
python setup.py develop