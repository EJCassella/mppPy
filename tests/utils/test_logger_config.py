import logging

from utils.logger_config import LogLevel, setup_logger


def test_logger_name_and_level():
	logger = setup_logger(level=LogLevel.INFO)
	assert logger.name == "mppPy"
	assert logger.level == logging.INFO
