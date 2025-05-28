from typing import Optional, List
from types import TracebackType

from controllers.interfaces import (
	SourcemeterContext,
	SourcemeterController,
	sourcemeterOutput,
	sourcemeterMode,
	sweepDirection,
)

from utils.logger_config import setup_logger

logger = setup_logger()

DEFAULT_VOLTAGE_PROTECTION = 5.0


class dummyK2400Context(SourcemeterContext):
	def __init__(self, address: Optional[str]):
		if address:
			self.address = "GPIB0::" + address + "::INSTR"
		else:
			raise ValueError(
				"Keithley GPIB connection could not be initiated without a provided GPIB address. Run mppPy.py -h for more information."
			)
		self.resource = None

	def __enter__(self) -> None:
		logger.info(f"Keithley acquired at address {self.address}.")

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		logger.info(f"Released Keithley at address {self.address}.")


class dummyK2400Controller(SourcemeterController):
	def __init__(self):
		self._voltage_protection: float = DEFAULT_VOLTAGE_PROTECTION
		logger.info("Initialising dummy sourcemeter.")
		self.reset()
		self.configure_data_output()
		logger.info("dummySourcemeter initialised.")

	def reset(self):
		logger.info("Resetting...")

	@property
	def voltage_protection(self) -> float:
		return self._voltage_protection

	@voltage_protection.setter
	def voltage_protection(self, voltage: float):
		if voltage > DEFAULT_VOLTAGE_PROTECTION:
			self._voltage_protection = DEFAULT_VOLTAGE_PROTECTION
			logger.warning("Trying to set voltage protection too high. Limiting voltage to 5 V.")
		elif voltage <= 0:
			self._voltage_protection = DEFAULT_VOLTAGE_PROTECTION
			logger.warning("Trying to set voltage protection too low. Setting voltage limit to 5 V.")
		else:
			self._voltage_protection = voltage
			logger.info(f"Setting voltage limit to {voltage} V.")

	def configure_data_output(self):
		logger.info("Sourcemeter set to output current, voltage, time.")

	def set_sm_output(self, output: sourcemeterOutput, value: float, mode: sourcemeterMode):
		logger.info(f":source:function {output.value}")
		logger.info(f":source:{output.value}:mode {mode.value}")
		logger.info(f":source:{output.value} {value}")
		# Implement error handling

	def read_output(self) -> List[float]:
		logger.info("Beep boop, reading current, voltage, time.")
		return [0.004, 0.96, 1.0]

	# TO DO: implement dummy setters to change output values

	def find_open_circuit_voltage(self):
		self.set_sm_output(output=sourcemeterOutput.CURRENT, value=0, mode=sourcemeterMode.FIXED)
		_, Voc, _ = self.read_output()
		logger.info(f"Beep boop, open circuit voltage found to be {Voc}.")
		return Voc

	def jv_sweep(self, max_voltage: float, sweep_direction: sweepDirection):
		if sweep_direction == sweepDirection.FORWARD:
			logger.info(f"Sweeping voltage value from 0V to {max_voltage}.")
		elif sweep_direction == sweepDirection.REVERSE:
			logger.info(f"Sweeping voltage value from {max_voltage} to 0V.")
		elif sweep_direction == sweepDirection.BOTH:
			logger.info(f"Sweeping voltage value from 0V to {max_voltage}V.")
			logger.info(f"Sweeping voltage value from {max_voltage}V to 0V.")
		# TO DO: return proxy JV array for MPP calculation
