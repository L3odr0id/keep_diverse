import time
import lzma

from textdistance import LZMANCD

from .file_paths import file_paths


def fast_lzma_distance(x: str, y: str) -> float:
    bx = bytes(x, "utf-8")
    by = bytes(y, "utf-8")
    bxy = bytes(x + y, "utf-8")
    cx = len(lzma.compress(bx))
    cy = len(lzma.compress(by))
    cxy = len(lzma.compress(bxy))
    return (cxy - min(cx, cy)) / max(cx, cy)


def honest_lzma_distance(x: str, y: str) -> float:
    bx = bytes(x, "utf-8")
    by = bytes(y, "utf-8")
    bxy = bytes(x + y, "utf-8")
    byx = bytes(y + x, "utf-8")
    cx = len(lzma.compress(bx))
    cy = len(lzma.compress(by))
    cxy = len(lzma.compress(bxy))
    cyx = len(lzma.compress(byx))
    return (min(cxy, cyx) - min(cx, cy)) / max(cx, cy)


def denis_impl_lzma_distance(x: str, y: str) -> float:
    bx = bytes(x, "utf-8")
    by = bytes(y, "utf-8")
    bxy = bytes(x + y, "utf-8")
    byx = bytes(y + x, "utf-8")
    bxx = bytes(x + x, "utf-8")
    byy = bytes(y + y, "utf-8")
    cx = len(lzma.compress(bx))
    cy = len(lzma.compress(by))
    cxx = len(lzma.compress(bxx))
    cyy = len(lzma.compress(byy))
    cxy = len(lzma.compress(bxy))
    cyx = len(lzma.compress(byx))
    return (min(cxy, cyx) - min(cxx, cyy)) / max(cx, cy)


def run_just_distance():
    distance_funs = [
        denis_impl_lzma_distance,
        honest_lzma_distance,
        LZMANCD().distance,
        fast_lzma_distance,
    ]
    algo_names = [
        "denis_impl_lzma_distance",
        "honest_lzma_distance",
        "LZMANCD",
        "fast_lzma_distance",
    ]

    files_len = 50
    file_paths_list = file_paths()[:files_len]
    file_contents = []
    for path in file_paths_list:
        with open(path, "r", encoding="utf-8") as file:
            file_contents.append(file.read())

    for distance, algo_name in zip(distance_funs, algo_names):
        start_time = time.perf_counter()

        for i in range(len(file_contents)):
            for j in range(i + 1, len(file_contents)):
                distance(file_contents[i], file_contents[j])

        end_time = time.perf_counter()
        print(
            f"Files count: {files_len}. Algo: {algo_name}. "
            f"Time: {end_time - start_time:.4f} seconds."
        )


if __name__ == "__main__":
    run_just_distance()
