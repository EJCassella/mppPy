from utils.logger_config import setup_logger


def sample_func(a: int, b: int) -> int:
	return a + b


def main() -> None:
	print(sample_func(2, 7))
	logger = setup_logger()
	logger.info("Logger initiated.")


if __name__ == "__main__":
	main()
