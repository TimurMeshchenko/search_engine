## Запуск

poetry run python manage.py runserver

poetry install
poetry run python -m uvicorn store.asgi:application --reload --port 8001
poetry run ./run_with_reload.sh
