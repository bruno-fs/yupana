#!/bin/bash
set -x

cp -f config/.host_env ../../insights-host-inventory/.env
cd ../../insights-host-inventory/
. .env

pipenv install --dev
pipenv run python manage.py db upgrade
pipenv run make run_inv_mq_service
