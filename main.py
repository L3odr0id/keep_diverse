import argparse
import logging
import os

from keep_diverse.filter_args import add_filter_args
from keep_diverse.path_args import add_path_arguments
from keep_diverse.knee_plot import KneePlot, NoOutputKneePlot, DisplayKneeArgs
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.logger import configure_logger
from keep_diverse.keep_diverse import keep_diverse
from keep_diverse.counter_report import CounterReport, NoCounterReport


def main() -> None:
    configure_logger(
        format="%(asctime)s - %(relativeCreated)d ms - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="Texts filter utility")
    add_path_arguments(parser)
    add_filter_args(parser)
    args = parser.parse_args()

    file_paths = [
        os.path.join(args.dir, name)
        for name in os.listdir(args.dir)
        if os.path.isfile(os.path.join(args.dir, name))
    ]

    if args.max_files is not None:
        file_paths = file_paths[: args.max_files]

    knee_plot = (
        NoOutputKneePlot()
        if args.output_plot_path is None
        else KneePlot(
            output_file=args.output_plot_path,
            display_knee_args=DisplayKneeArgs(
                total_files_count=len(file_paths),
                split_by=args.split_by,
                relative_eps=args.relative_eps,
                max_tries=args.max_tries_per_filter_iteration,
                min_indices_count=args.min_indices_count,
                filter_rounds=args.filter_rounds,
            ),
        )
    )

    filtered_files_list = FilteredFilesList(
        output_file_path=args.output_file_path,
    )

    counter_report = (
        NoCounterReport()
        if args.counter_report_path is None
        else CounterReport(
            output_file_path=args.counter_report_path,
        )
    )

    keep_diverse(
        file_paths=file_paths,
        filter_rounds=args.filter_rounds,
        split_by=args.split_by,
        relative_eps=args.relative_eps,
        max_tries=args.max_tries_per_filter_iteration,
        min_indices_count=args.min_indices_count,
        knee_plot=knee_plot,
        filtered_files_list=filtered_files_list,
        counter_report=counter_report,
    )


if __name__ == "__main__":
    main()
