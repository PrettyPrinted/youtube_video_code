docker compose up -d
uv run flask run
uv run celery -A make_celery worker -l info
uv run celery -A make_celery beat -S redbeat.RedBeatScheduler -l info