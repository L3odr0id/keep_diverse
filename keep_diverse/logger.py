import logging


def get_logger():
    return logging.getLogger("keep_diverse")


def configure_logger(
    format: str = "%(asctime)s - %(relativeCreated)d ms - %(levelname)s - %(funcName)s - %(message)s",
    level: int = logging.INFO,
):
    keep_diverse_logger = get_logger()

    keep_diverse_logger.setLevel(level)

    keep_diverse_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    keep_diverse_logger.addHandler(handler)

    keep_diverse_logger.propagate = False
