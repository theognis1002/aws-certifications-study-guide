#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic --no-input
uvicorn aws_quiz.asgi:application --host 0.0.0.0 --reload

exec "$@"
