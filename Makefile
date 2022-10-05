build:
	docker compose up --build

run:
	docker compose up

destroy:
	docker compose down -v

rebuild: destroy build

makemigrations:
	docker compose run web python manage.py makemigrations
mm: makemigrations

migrate:
	docker compose run web python manage.py migrate
m: migrate

bash:
	docker compose run web bash
b: bash
