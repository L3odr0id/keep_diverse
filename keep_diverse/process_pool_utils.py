import signal
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Type

from .logger import get_logger


@contextmanager
def _safe_pool_executor(executor_class: Type, max_workers: int):
    # original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    executor = executor_class(max_workers=max_workers)
    # signal.signal(signal.SIGINT, original_sigint_handler)

    try:
        yield executor
    except KeyboardInterrupt:
        get_logger().info("\nKeyboardInterrupt received, shutting down executor...")
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    else:
        executor.shutdown(wait=True)


@contextmanager
def safe_process_pool_executor(max_workers: int):
    with _safe_pool_executor(ProcessPoolExecutor, max_workers) as executor:
        yield executor


@contextmanager
def safe_thread_pool_executor(max_workers: int):
    with _safe_pool_executor(ThreadPoolExecutor, max_workers) as executor:
        yield executor
