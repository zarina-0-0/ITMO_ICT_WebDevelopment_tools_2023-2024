from sqlmodel import Session, create_engine
from sqlalchemy import text
from bs4 import BeautifulSoup


DATABASE_URL = "postgresql://a1111@localhost:5432/workout_db"

engine = create_engine(DATABASE_URL)


def save_page(url: str, title: str):
    """Сохраняет результат парсинга в базу данных."""
    with Session(engine) as session:
        session.execute(
            text("""
                INSERT INTO parsed_pages (url, title)
                VALUES (:url, :title)
            """),
            {"url": url, "title": title}
        )
        session.commit()


def parse_html(url: str, html: str):
    """Получает заголовок страницы из HTML."""
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title = "Без заголовка"

    return url, title