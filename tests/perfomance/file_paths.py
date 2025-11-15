import os
from pathlib import Path


def file_paths():
    test_dir = Path(__file__).parent.parent / "data"

    file_paths = sorted([str(test_dir / name) for name in os.listdir(test_dir)])[:100]

    return file_paths


def file_paths_with_idxs():
    return [(idx, path) for idx, path in enumerate(file_paths())]
