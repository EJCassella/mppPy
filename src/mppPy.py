import sys

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


from controllers.interfaces import (
	sweepDirection,
)

from pydantic import ValidationError

from contextlib import ExitStack

""" For 3-cells expect 1.2V * 3 max voltage, protection set in Volts and 24 mA/cm^2 * 2.4cm^2, set in Amps. Absolute hard limits (enough for 5-cell design) set to 6.5 V and 0.288 A in K2400 class. Only change the hard limit if absolutely necessary, i.e. active areas greater than 11.5 cm^2 or more than 5 cells. Keep the protection and compliance as low as necessary for you application for safety during measurements."""
VOLTAGE_PROTECTION = 3.6
CURRENT_COMPLIANCE = 0.058


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

	logger = setup_logger(level=LogLevel.INFO)
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

				sm.jv_sweep(max_voltage=1.2, sweep_direction=sweepDirection.BOTH)

				# TO DO
				# do some maximum power point tracking....
				# mpptracker = MPPTracker(sourcemeter = sm, shutter = shutter, cell_area=tracker_config.device_area_cm2, tracking_time=tracker_config.tracking_time_seconds)
				# mpptracker.run()

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
