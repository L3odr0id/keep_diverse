import argparse


def add_path_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output-plot-path", type=str, required=False, default=None)
    parser.add_argument("--output-file-path", type=str, required=True)
    parser.add_argument("--counter-report-path", type=str, required=False, default=None)
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--max-files", type=int, required=False, default=None)
