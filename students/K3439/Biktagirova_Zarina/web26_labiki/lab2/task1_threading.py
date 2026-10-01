import threading
import time


N = 10_000_000_000_000
TASKS = 4


def calculate_sum(start: int, end: int) -> int:
    """Вычисляет сумму чисел от start до end включительно."""
    count = end - start + 1
    return (start + end) * count // 2


def worker(start: int, end: int, results: list, index: int):
    results[index] = calculate_sum(start, end)


def main():
    chunk_size = N // TASKS
    threads = []
    results = [0] * TASKS

    start_time = time.perf_counter()

    for i in range(TASKS):
        start = i * chunk_size + 1

        if i == TASKS - 1:
            end = N
        else:
            end = (i + 1) * chunk_size

        thread = threading.Thread(
            target=worker,
            args=(start, end, results, i)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Сумма: {total}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    main()