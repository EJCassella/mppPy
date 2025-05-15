import logging
from enum import Enum


class LogLevel(Enum):
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL


def setup_logger(logfile: str | None = None, level: LogLevel = LogLevel.INFO) -> logging.Logger:
	logger = logging.getLogger("mppPy")
	logger.setLevel(level.value)

	formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d - %H:%M:%S")

	if logger.hasHandlers():
		logger.handlers.clear()

	ch = logging.StreamHandler()
	ch.setFormatter(formatter)
	logger.addHandler(ch)

	if logfile:
		fh = logging.FileHandler(logfile)
		fh.setFormatter(formatter)
		logger.addHandler(fh)

	return logger
