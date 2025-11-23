import numpy as np
import os
import tempfile
from collections import Counter
from concurrent.futures import as_completed
from scipy.stats import sem, tstd

from .knee_plot import Plot
from .filtered_files_list import FilteredFilesList
from .counter_report import CounterReport
from .knee import Knee
from .process_pool_utils import safe_process_pool_executor
from .compressed_file_lens import compressed_file_lens_list
from .filtration_round import filtration_round
from .logger import get_logger


def keep_diverse(
    file_paths: list[str],
    filter_rounds: int,
    split_by: int,
    relative_eps: float,
    max_tries: int,
    min_indices_count: int,
    knee_plot: Plot,
    filtered_files_list: FilteredFilesList,
    counter_report: CounterReport,
    processes_count: int = 10,
):
    keep_diverse_logger = get_logger()

    compressed_lens = compressed_file_lens_list(file_paths)
    comp_lens_np_arr = np.array(compressed_lens, dtype=np.int64)

    file_path = os.path.join(tempfile.gettempdir(), "compressed_file_lens_cached.npy")
    np.save(file_path, comp_lens_np_arr)

    keep_diverse_logger.info("Saved all lens to file")

    removes_counter = Counter()
    for fp in file_paths:
        removes_counter[fp] = 0

    knees_list = []
    sems_list = []

    finished_rounds = 0
    with safe_process_pool_executor(max_workers=processes_count) as executor:
        futures = [
            executor.submit(
                filtration_round,
                file_paths=file_paths,
                split_by=split_by,
                relative_eps=relative_eps,
                max_tries=max_tries,
                min_indices_count=min_indices_count,
                compressed_lens_file_path=file_path,
            )
            for _ in range(filter_rounds)
        ]

        for future in as_completed(futures):
            files_idxs_to_remove = future.result()
            files_to_remove = [file_paths[i] for i in files_idxs_to_remove]
            removes_counter.update(files_to_remove)

            finished_rounds += 1

            knee = Knee(removes_counter)
            knees_list.append(knee.value)

            sem_value = sem(knees_list)
            sems_list.append(sem_value)

            knee_plot.draw(knee, sems_list, finished_rounds)

            filtered_files_list.save(knee)
            counter_report.save(removes_counter)

            keep_diverse_logger.info(
                f"Filter. Finished round {finished_rounds} / {filter_rounds}"
            )
