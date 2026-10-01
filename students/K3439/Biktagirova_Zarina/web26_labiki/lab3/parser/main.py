import os

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, create_engine
from sqlalchemy import text


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://a1111@localhost:5432/workout_db"
)

engine = create_engine(DATABASE_URL)


app = FastAPI(
    title="Parser API",
    description="Парсер веб-страниц из лабораторной работы 2"
)


def parse_html(url: str, html: str):
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title = "Без заголовка"

    return url, title


def save_page(url: str, title: str):
    with Session(engine) as session:
        session.execute(
            text("""
                INSERT INTO parsed_pages (url, title)
                VALUES (:url, :title)
            """),
            {
                "url": url,
                "title": title
            }
        )
        session.commit()


@app.post("/parse")
def parse(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        url, title = parse_html(url, response.text)
        save_page(url, title)

        return {
            "message": "Parsing completed",
            "url": url,
            "title": title
        }

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )