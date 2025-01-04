## Запуск

poetry run python manage.py runserver

poetry install
poetry run python -m uvicorn search_engine.asgi:application --reload --port 8005
poetry run ./run_with_reload.sh

Прод:
poetry run python -m uvicorn search_engine.asgi:application --port 8005

# Webpack optimization

docker build -f Dockerfile.webpack -t search_engine_webpack .
docker run --name search_engine_webpack_container -p 8080:8080 -v ./optimized:/app/optimized -v ./webpack.config.js:/app/webpack.config.js -d search_engine_webpack

sudo docker exec -it search_engine_webpack_container bash
npx webpack

sudo docker stop search_engine_webpack_container
sudo docker rm search_engine_webpack_container
sudo docker rmi search_engine_webpack