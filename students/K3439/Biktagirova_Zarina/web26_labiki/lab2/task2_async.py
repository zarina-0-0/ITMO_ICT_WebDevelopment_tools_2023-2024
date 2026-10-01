import asyncio
import time

import aiohttp

from task2_common import parse_html, save_page


URLS = [
    "https://example.com",
    "https://www.python.org/",
    "https://docs.python.org/3/",
    "https://www.iana.org/",
]


async def parse_and_save(
    session: aiohttp.ClientSession,
    url: str
):
    """Асинхронно загружает страницу, получает заголовок и сохраняет его в БД."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            response.raise_for_status()

            html = await response.text()

            url, title = parse_html(url, html)
            save_page(url, title)

            print(f"{url} -> {title}")

    except Exception as e:
        print(f"{url} -> ошибка: {e}")


async def main():
    start_time = time.perf_counter()

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            parse_and_save(session, url)
            for url in URLS
        ]

        await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start_time

    print(f"\nВремя выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    asyncio.run(main())