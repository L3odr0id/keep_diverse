from concurrent.futures import as_completed
from .process_pool_utils import safe_thread_pool_executor


def read_one_file(file_path: str, idx: int) -> tuple[int, str]:
    with open(file_path) as f:
        return (idx, f.read())


def read_files(
    file_paths: list[tuple[int, str]], max_workers: int = 10
) -> list[tuple[int, str]]:
    results = []
    with safe_thread_pool_executor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(read_one_file, file_path, idx)
            for idx, file_path in file_paths
        ]

        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: x[0])

    return results
