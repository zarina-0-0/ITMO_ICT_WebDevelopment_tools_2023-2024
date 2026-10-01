import threading
import time

import requests

from task2_common import parse_html, save_page

URLS = [
    "https://example.com",
    "https://www.python.org/",
    "https://docs.python.org/3/",
    "https://www.iana.org/",
]


def parse_and_save(url: str):
    """Загружает страницу, получает заголовок и сохраняет его в БД."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        url, title = parse_html(url, response.text)
        save_page(url, title)

        print(f"{url} -> {title}")

    except Exception as e:
        print(f"{url} -> ошибка: {e}")


def main():
    threads = []

    start_time = time.perf_counter()

    for url in URLS:
        thread = threading.Thread(
            target=parse_and_save,
            args=(url,)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start_time

    print(f"\nВремя выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    main()