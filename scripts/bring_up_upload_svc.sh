#!/bin/bash
set -x
upload_dir_path='insights-ingress-go'
cp config/.upload_env ${upload_dir_path}/.env
cd $upload_dir_path
pipenv run docker-compose up
