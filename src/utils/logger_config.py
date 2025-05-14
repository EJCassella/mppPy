import logging


def setup_logger(logfile: str | None = None) -> logging.Logger:
	logger = logging.getLogger("mppPy")
	logger.setLevel(logging.INFO)

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
