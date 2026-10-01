import os

import requests
from celery import Celery


CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0"
)

CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/0"
)


celery_app = Celery(
    "parser_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)


@celery_app.task
def parse_url_task(url: str):
    response = requests.post(
        "http://parser:8001/parse",
        params={"url": url},
        timeout=30
    )

    response.raise_for_status()

    return response.json()