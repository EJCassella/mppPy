import sys

from utils.logger_config import setup_logger
from utils.parser import parse_arguments


def sample_func(a: int, b: int) -> int:
	return a + b


def main() -> None:
	print(sample_func(2, 7))
	logger = setup_logger()
	logger.info("Log initiated.")
	# parse args
	args = parse_arguments(sys.argv[1:])
	print(args)
	# pass args to core
	# use args to setup hardware (sourcemeter and shutter[opt])
	# run tracking algorithm
	# plotting and logging
	# shutdown equipment


if __name__ == "__main__":
	main()
