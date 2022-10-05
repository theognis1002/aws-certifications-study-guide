#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
uvicorn aws_quiz.asgi:application --host 0.0.0.0 --reload

exec "$@"
