import sys

from utils.logger_config import setup_logger, LogLevel
from utils.parser import parse_arguments
from utils.validator import UserSetting

from pyvisa import VisaIOError
from nidaqmx.errors import DaqError  # type: ignore

# from controllers.K2400 import K2400Context
# from controllers.shutterUSB6501 import shutterUSB6501

from controllers.dummyK2400 import dummyK2400Context, dummyK2400Controller
from controllers.dummyShutter import dummyShutter

from pydantic import ValidationError

from contextlib import ExitStack


def main() -> None:
	args = parse_arguments(sys.argv[1:])

	try:
		tracker_config = UserSetting(
			tracking_time_seconds=args.tracking_time_seconds,
			device_area_cm2=args.device_area_cm2,
			gpib_address=args.gpib_address,
			shutter=args.shutter,
		)

	except ValidationError as e:
		print(f"The tracker configuration settings could not be validated: {e}.")
		sys.exit(1)

	logger = setup_logger(level=LogLevel.INFO)
	logger.info("Log initiated.")

	# use args to setup hardware (sourcemeter and shutter[opt])
	try:
		with ExitStack() as stack:
			stack.enter_context(dummyK2400Context(address=tracker_config.gpib_address))

			if tracker_config.shutter:
				stack.enter_context(dummyShutter(enabled=tracker_config.shutter))
			else:
				logger.info("Shutter control disabled.")

			# TO DO
			# do some maximum power point tracking....
			# mpptracker = MPPTracker(sourcemeter = sm, shutter = shutter, cell_area=tracker_config.device_area_cm2, tracking_time=tracker_config.tracking_time_seconds)
			# mpptracker.run()

	except VisaIOError:
		logger.error("Keithley communication error has occured. Exiting.")
	except DaqError:
		logger.error("Shutter communication error has occured. Exiting.")
	except Exception as e:
		logger.error(f"An unexpected error has occured: {e}")
	# finally:
	# shutdown interactive plot
	# close log file
	# write to console


# TO DO
# plotting and logging data


if __name__ == "__main__":
	main()
