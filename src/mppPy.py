import sys

from utils.logger_config import setup_logger
from utils.parser import parse_arguments
from utils.validator import UserSetting

from controllers.K2400 import K2400Context

from pydantic import ValidationError


def main() -> None:
	args = parse_arguments(sys.argv[1:])

	try:
		tracker_config = UserSetting(
			tracking_time_seconds=args.tracking_time_seconds,
			device_area_cm2=args.device_area_cm2,
			gpib_address=args.gpib_address,
			shutter=args.shutter,
		)
		print(tracker_config)

	except ValidationError as e:
		print(f"The tracker configuration settings could not be validated: {e}.")
		sys.exit(1)

	logger = setup_logger()
	logger.info("Log initiated.")

	# use args to setup hardware (sourcemeter and shutter[opt])
	with K2400Context(address=tracker_config.gpib_address) as keithley:
		logger.info("Keithley initiated.")


""" 
try:
	open keithley context using gpib address
		if shutter, open shutter using context manager
			run mpptracker fed with tracker config options (keithley, shutter, tracking_time, cell_area)
		else
			run mpptracker fed with tracker config options (keithley, shutter, tracking_time, cell_area)
except:
	kethley error
except:
	shutter error

"""
# run tracking algorithm
# plotting and logging
# shutdown equipment


if __name__ == "__main__":
	main()
