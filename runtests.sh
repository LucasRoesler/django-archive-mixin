#!/usr/bin/env sh
cd tests && coverage run --source=test_app manage.py test test_app
coverage report --fail-under=100