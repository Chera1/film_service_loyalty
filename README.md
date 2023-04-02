## Запуск локально
Firstly create env file src/core/.env with following parameters:
```shell
PROJECT_NAME - name of project
REDIS_HOST - Redis host
REDIS_PORT - Redis port
ELASTIC_HOST - Elasticsearch host
ELASTIC_PORT - Elasticsearch port
SENTRY_DSN - DSN for sentry
```
To run under uvicorn execute following commands:
```shell
uvicorn main:app --reload --host localhost --port 8009
```
To run under gunicorn execute following commands:
```shell
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8009
```
OpenApi documentation url: http://localhost:8009/api/openapi/


## Запуск в Docker
Предварительно необходимо в корне проекта создать файлы `admin.env` и `api.env`

Параметры `.env` файлов можно найти в
[admin_panel/README.md](./admin_panel/README.md) 
и [loyalty_api/README.md](./loyalty_api/README.md) соответственно.

Для запуска api в `Docker` необходимо выполнить команду
```shell
docker compose up --build
```

Адрес документации: http://localhost/api/openapi/
