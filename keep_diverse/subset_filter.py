def calculate_distance(
    i: int, j: int, x_cached_len: int, y_cached_len: int, x_text: str, y_text: str
) -> tuple[tuple[int, int], float]:
    from .compress_lzma import compress_lzma
    from .distance import fast_distance

    distance = fast_distance(
        x_len=x_cached_len,
        y_len=y_cached_len,
        xy_len=compress_lzma(bytes(x_text + y_text, "utf-8")),
    )
    return ((i, j), distance)


def calc_all_distances(
    files: list[tuple[int, str]],
    subset_compressed_caches: list[int],
    max_workers: int = 10,
) -> dict[tuple[int, int], float]:
    from concurrent.futures import as_completed
    from .process_pool_utils import safe_thread_pool_executor

    files_len = len(files)

    dist_dict = {}
    with safe_thread_pool_executor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                calculate_distance,
                i,
                j,
                subset_compressed_caches[i],
                subset_compressed_caches[j],
                files[i][1],
                files[j][1],
            )
            for i in range(files_len)
            for j in range(i, files_len)
        ]

        for future in as_completed(futures):
            (i, j), distance = future.result()
            dist_dict[(i, j)] = distance

    return dist_dict


def subset_filter(
    subset_file_paths: list[tuple[int, str]],
    relative_eps: float,
    max_tries: int,
    min_indices_count: int,
    subset_compressed_caches: list[int],
):
    from .read_files import read_files
    from .fast_pct_filter import FastPctFilter
    from .logger import get_logger

    dist_dict = calc_all_distances(
        files=read_files(subset_file_paths),
        subset_compressed_caches=subset_compressed_caches,
    )

    initial_idxs = list(range(len(subset_file_paths)))

    pct_filter = FastPctFilter(
        initial_indices=initial_idxs,
        relative_eps=relative_eps,
        max_tries=max_tries,
        min_indices_count=min_indices_count,
        text_set_distances=dist_dict,
    )

    while not pct_filter.is_finished:
        pct_filter.iterate()

    local_missing_idxs = [i for i in initial_idxs if i not in pct_filter.current_idxs]

    get_logger().info(
        f"Subset filter. Removed {len(local_missing_idxs)} files out of {len(subset_file_paths)}"
    )

    return [subset_file_paths[i][0] for i in local_missing_idxs]
