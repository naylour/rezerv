import logging

import colorlog

from config import LOGS_PATH

color_stream = colorlog.StreamHandler()
color_stream.setFormatter(
    colorlog.ColoredFormatter(
        "%(asctime)s %(log_color)s[%(levelname)-7s]%(reset)s %(log_color)s%(message)s",
        # datefmt=None,
        reset=True,
    )
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[color_stream, logging.FileHandler(LOGS_PATH)],
)

logger = logging.getLogger("log")
console = logging.getLogger("console")
