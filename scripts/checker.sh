#!/bin/bash

RUN_INTERNALLY="$1"

check_styling_and_unit_tests() {
    if [ -z "$RUN_INTERNALLY" ]; then
        source venv/bin/activate
    fi

    flake8 --ignore=E501,E271,E272,W602,W504 --exclude=venv
    cd test_project
    python manage.py makemigrations
    python manage.py migrate
    python manage.py test
}

check_styling_and_unit_tests
