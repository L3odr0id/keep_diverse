def split_list_by(elements: list, split_by: int) -> list:
    smaller_sets = []
    for i in range(0, len(elements), split_by):
        subset = elements[i : i + split_by]
        smaller_sets.append(subset)

    return smaller_sets


def select_subset_compressed_caches(
    files_set: list[tuple[int, str]], compressed_file_lens_cached
):
    return [compressed_file_lens_cached[file_tuple[0]] for file_tuple in files_set]


def filtration_round(
    file_paths: list[str],
    split_by: int,
    relative_eps: float,
    max_tries: int,
    min_indices_count: int,
    compressed_lens_file_path: str,
    max_workers: int = 10,
):
    import random
    import numpy as np
    from concurrent.futures import as_completed
    from .subset_filter import subset_filter
    from .sort_tuple import sort_tuple
    from .process_pool_utils import safe_thread_pool_executor

    compressed_file_lens_cached = np.load(compressed_lens_file_path)

    indexed_paths = list(enumerate(file_paths))
    random.shuffle(indexed_paths)

    smaller_sets: list[list[tuple[int, str]]] = split_list_by(indexed_paths, split_by)

    all_files_to_remove = []
    with safe_thread_pool_executor(max_workers=max_workers) as executor:
        futures = []
        for i in range(len(smaller_sets)):
            files_set = smaller_sets[i]
            files_set = sort_tuple(files_set)
            subset_compressed_caches = select_subset_compressed_caches(
                files_set, compressed_file_lens_cached
            )

            futures.append(
                executor.submit(
                    subset_filter,
                    subset_file_paths=files_set,
                    relative_eps=relative_eps,
                    max_tries=max_tries,
                    min_indices_count=min_indices_count,
                    subset_compressed_caches=subset_compressed_caches,
                )
            )

        for future in as_completed(futures):
            files_to_remove = future.result()
            all_files_to_remove.extend(files_to_remove)

    return all_files_to_remove
