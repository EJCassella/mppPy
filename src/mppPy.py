import sys

from core.core import MaximumPowerPointTracker

from utils.logger_config import setup_logger, LogLevel
from utils.parser import parse_arguments
from utils.validator import UserSetting
from utils.custom_exceptions import OutputLimitsExceededError

from pyvisa import VisaIOError
from nidaqmx.errors import DaqError  # type: ignore

from controllers.K2400 import K2400Context, K2400Controller
from controllers.shutterUSB6501 import shutterUSB6501

from controllers.dummyK2400 import dummyK2400Context, dummyK2400Controller
from controllers.dummyShutter import dummyShutter

from pydantic import ValidationError

from contextlib import ExitStack


from controllers.interfaces import (
	sweepDirection,
)

from utils.constants import VOLTAGE_PROTECTION, CURRENT_COMPLIANCE

import os

print(os.getcwd())


def main() -> None:
	args = parse_arguments(sys.argv[1:])

	try:
		tracker_config = UserSetting(
			tracking_time_seconds=args.tracking_time_seconds,
			device_area_cm2=args.device_area_cm2,
			gpib_address=args.gpib_address,
			shutter=args.shutter,
			dummy=args.dummyMode,
			metadata=args.metadata,
		)

	except ValidationError as e:
		print(f"The tracker configuration settings could not be validated: {e}.")
		sys.exit(1)

	logger = setup_logger(level=LogLevel.DEBUG)
	logger.info("Log initiated.")

	if tracker_config.dummy:
		try:
			with ExitStack() as stack:
				resource = stack.enter_context(dummyK2400Context(address=tracker_config.gpib_address))

				if tracker_config.shutter:
					stack.enter_context(dummyShutter(enabled=tracker_config.shutter))
				else:
					logger.info("Shutter control disabled.")

				sm = dummyK2400Controller(
					resource=resource,
					voltage_protection=VOLTAGE_PROTECTION,
					current_compliance=CURRENT_COMPLIANCE,
				)

				mppt = MaximumPowerPointTracker(
					sourcemeter=sm,
					cell_area=tracker_config.device_area_cm2,
					tracking_time=tracker_config.tracking_time_seconds,
					dummyMode=tracker_config.dummy,
				)

				mppt.find_initial_vmpp()

		except OutputLimitsExceededError as e:
			logger.error(f"Safe output limits exceeded: {e}")
		except Exception as e:
			logger.error(f"An unexpected error has occured: {e}")
		finally:
			logger.info("Program finished.")
			# shutdown interactive plot
			# close log file
			# write to console

	else:
		try:
			with ExitStack() as stack:
				resource = stack.enter_context(K2400Context(address=tracker_config.gpib_address))

				if tracker_config.shutter:
					stack.enter_context(shutterUSB6501(enabled=tracker_config.shutter))
				else:
					logger.info("Shutter control disabled.")

				sm = K2400Controller(
					resource=resource,
					voltage_protection=VOLTAGE_PROTECTION,
					current_compliance=CURRENT_COMPLIANCE,
				)

		except VisaIOError:
			logger.error("Keithley communication error has occured. Exiting.")
		except DaqError:
			logger.error("Shutter communication error has occured. Exiting.")
		except OutputLimitsExceededError as e:
			logger.error(f"Safe output limits exceeded: {e}")
		except Exception as e:
			logger.error(f"An unexpected error has occured: {e}")
		finally:
			logger.info("Program finished.")


if __name__ == "__main__":
	main()
