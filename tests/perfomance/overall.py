import os
import time
import tempfile
import logging

import cProfile

from .file_paths import file_paths
from keep_diverse.knee_plot import KneePlot, DisplayKneeArgs, NoOutputKneePlot
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.logger import configure_logger
from keep_diverse.keep_diverse import keep_diverse
from keep_diverse.counter_report import CounterReport


def overall():
    configure_logger(
        level=logging.INFO,
    )

    files = file_paths()

    temp_dir = os.getcwd()  # tempfile.TemporaryDirectory()
    output_plot_path = os.path.join(temp_dir, "knee_plot.svg")
    output_file_path = os.path.join(temp_dir, "filtered_files.txt")
    counter_report_path = os.path.join(temp_dir, "counter_report.json")
    # Default parameters (from filter_args.py)
    split_by = 50
    relative_eps = 0.00001
    max_tries = 10
    min_indices_count = 10
    filter_rounds = 10

    knee_plot = KneePlot(
        output_file=output_plot_path,
        display_knee_args=DisplayKneeArgs(
            total_files_count=len(files),
            split_by=split_by,
            relative_eps=relative_eps,
            max_tries=max_tries,
            min_indices_count=min_indices_count,
            filter_rounds=filter_rounds,
        ),
    )

    filtered_files_list = FilteredFilesList(
        output_file_path=output_file_path,
    )

    counter_report = CounterReport(
        output_file_path=counter_report_path,
    )

    start_time = time.perf_counter()

    keep_diverse(
        file_paths=files,
        filter_rounds=filter_rounds,
        split_by=split_by,
        relative_eps=relative_eps,
        max_tries=max_tries,
        min_indices_count=min_indices_count,
        knee_plot=knee_plot,
        filtered_files_list=filtered_files_list,
        counter_report=counter_report,
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print(f"Performance Test Results:")
    print(f"  Files processed: {len(files)}")
    print(f"  Split by: {split_by}")
    print(f"  Filter rounds: {filter_rounds}")
    print(f"  Execution time: {elapsed_time:.4f} seconds")

    return elapsed_time


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    overall()

    profiler.disable()
    profiler.dump_stats("program.prof")
