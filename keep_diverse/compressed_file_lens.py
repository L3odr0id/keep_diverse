def compressed_file_len(file_path: str, initial_idx: int) -> tuple[int, int]:
    from .compress_lzma import compress_lzma

    with open(file_path, "rb") as f:
        return (initial_idx, compress_lzma(f.read()))


def os_cpu_count_threads() -> int:
    import os

    return min(os.cpu_count() - 1, 1)


def compressed_file_lens_list(
    file_paths: list[str], max_workers: int = os_cpu_count_threads()
):
    from concurrent.futures import as_completed
    from .process_pool_utils import safe_thread_pool_executor

    results = {}
    with safe_thread_pool_executor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(compressed_file_len, file_path, i)
            for i, file_path in enumerate(file_paths)
        ]

        for future in as_completed(futures):
            initial_idx, compressed_len = future.result()
            results[initial_idx] = compressed_len

    return [results[i] for i in range(len(file_paths))]
