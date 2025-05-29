from typing import Optional, Sequence, Any, cast
from types import TracebackType

from controllers.interfaces import (
	SourcemeterContext,
	SourcemeterController,
	sourcemeterOutput,
	sourcemeterMode,
	sweepDirection,
)

from utils.logger_config import setup_logger
from utils.custom_exceptions import OutputLimitsExceededError
from utils.constants import SWEEP_RATE

from pyvisa.resources import GPIBInstrument

logger = setup_logger()


class dummyK2400Context(SourcemeterContext):
	def __init__(self, address: Optional[str]):
		if address:
			self.address = "GPIB0::" + address + "::INSTR"
		else:
			raise ValueError(
				"Keithley GPIB connection could not be initiated without a provided GPIB address. Run mppPy.py -h for more information."
			)
		self.resource = None

	def __enter__(self) -> GPIBInstrument:
		logger.info(f"Keithley acquired at address {self.address}.")
		self.resource = self.address
		self.resource = cast(GPIBInstrument, self.resource)
		return self.resource

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		logger.info(f"Released Keithley at address {self.address}.")


class dummyK2400Controller(SourcemeterController):
	def __init__(self, resource: GPIBInstrument, voltage_protection: float, current_compliance: float):
		self.max_voltage: float = 6  # max needed for 5-cell
		self.max_current: float = 0.288  # max needed for 5-cell
		self._voltage_protection: float
		self._current_compliance: float

		logger.info("Initialising dummy sourcemeter.")

		self.reset()
		self.set_voltage_protection(voltage_protection)
		self.set_current_compliance(current_compliance)
		self.configure_data_output()

		logger.info("dummySourcemeter initialised.")

	def reset(self):
		logger.info("Resetting...")

	def set_voltage_protection(self, voltage_protection: float):
		self.voltage_protection = voltage_protection

	@property
	def voltage_protection(self) -> float:
		return self._voltage_protection

	@voltage_protection.setter
	def voltage_protection(self, voltage: float):
		if voltage > self.max_voltage:
			self._voltage_protection = self.max_voltage
			logger.warning(f"Trying to set voltage protection too high. Limiting voltage to {self.max_voltage} V.")
		elif voltage <= 0:
			self._voltage_protection = self.max_voltage
			logger.warning(f"Trying to set voltage protection too low. Setting voltage limit to {self.max_voltage} V.")
		else:
			self._voltage_protection = voltage
			logger.info(f"Setting voltage limit to {voltage} V.")

	def set_current_compliance(self, current_compliance: float):
		self.current_compliance = current_compliance

	@property
	def current_compliance(self):
		return self._current_compliance

	@current_compliance.setter
	def current_compliance(self, current: float):
		if current > self.max_current:
			self._current_compliance = self.max_current
			logger.warning(
				f"Trying to set current protection too high. Limiting current compliance to {self.max_current} A."
			)
		elif current <= 0:
			self._current_compliance = self.max_current
			logger.warning(
				f"Trying to set current protection too low. Setting current compliance to {self.max_current} V."
			)
		else:
			self._current_compliance = current
			logger.info(f"Setting current compliance to {current} V.")

	def configure_data_output(self):
		logger.info("Sourcemeter set to output current, voltage, time.")

	def set_sm_output(
		self,
		output: sourcemeterOutput,
		value: float,
		mode: sourcemeterMode,
		sweepdir: sweepDirection = sweepDirection.FORWARD,
		sweep_rate: float = SWEEP_RATE,
	):
		if str(output.value) == "current":
			max_value = self.current_compliance
		else:
			max_value = self.voltage_protection

		try:
			if not (0 <= value <= max_value):
				raise OutputLimitsExceededError(
					f"Attempted to set {output.value} to {value} which exceeds maximum safe value of {max_value}."
				)

			elif str(mode.value) == "sweep":
				logger.debug(f":source:function {output.value}")
				logger.debug(f":source:{output.value}:mode {mode.value}")
				logger.debug(":source:sweep:spacing linear")
				logger.debug(":source:delay 0.05")  # Settling time in seconds

				nPoints = value / (0.05 * sweep_rate)  # voltage (V) / (delay (S) * sweep_rate (V/s))

				logger.debug(f":trigger:count {nPoints}")
				logger.debug(f":source:sweep:points {nPoints}")

				if sweepdir == sweepDirection.FORWARD:
					logger.debug(f":source:{output.value}:start 0.0")
					logger.debug(f":source:{output.value}:stop {value}")
					logger.info(f"Sweeping {output.value} value from 0 to {value}.")

				elif sweepdir == sweepDirection.REVERSE:
					logger.debug(f":source:{output.value}:start {value}")
					logger.debug(f":source:{output.value}:stop 0.0")
					logger.info(f"Sweeping {output.value} value from {value} to 0.")

			else:
				logger.debug(f":source:function {output.value}")
				logger.debug(f":source:{output.value}:mode {mode.value}")
				logger.debug(f":source:{output.value} {value}")
				logger.debug(":output on")

		except OutputLimitsExceededError as e:
			raise e

	def read_output(self) -> Sequence[Any]:
		logger.info("Beep boop, reading current, voltage, time.")
		return [0.004, 0.96, 1.0]

	# TO DO: implement dummy setters to change output values
