import asyncio
import time


N = 10_000_000_000_000
TASKS = 4


async def calculate_sum(start: int, end: int) -> int:
    """Вычисляет сумму чисел от start до end включительно."""
    count = end - start + 1
    return (start + end) * count // 2


async def main():
    chunk_size = N // TASKS
    ranges = []

    for i in range(TASKS):
        start = i * chunk_size + 1

        if i == TASKS - 1:
            end = N
        else:
            end = (i + 1) * chunk_size

        ranges.append((start, end))

    start_time = time.perf_counter()

    tasks = [
        calculate_sum(start, end)
        for start, end in ranges
    ]

    results = await asyncio.gather(*tasks)

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Сумма: {total}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    asyncio.run(main())