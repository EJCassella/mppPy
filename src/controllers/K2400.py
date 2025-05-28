import pyvisa as visa

from typing import Optional, cast, List
from types import TracebackType

from controllers.interfaces import (
	SourcemeterContext,
	SourcemeterController,
	sourcemeterOutput,
	sweepDirection,
	sourcemeterMode,
)

from utils.logger_config import setup_logger

from pyvisa.resources import GPIBInstrument, MessageBasedResource


logger = setup_logger()


class K2400Context(SourcemeterContext):
	resource: Optional[GPIBInstrument]
	address: str

	def __init__(self, address: str):
		if address:
			self.address = f"GPIB0::{address}::INSTR"
		else:
			raise ValueError(
				"Keithley GPIB connection could not be initiated without a provided GPIB address. Run mppPy.py -h for more information."
			)
		self.resource = None

	def __enter__(self) -> GPIBInstrument:
		rm = visa.ResourceManager()
		try:
			self.resource = cast(
				GPIBInstrument, rm.open_resource(resource_name=self.address, timeout=60000, _read_termination="\n")
			)
			logger.info(f"Keithley acquired at address {self.address}.")
			return self.resource
		except visa.VisaIOError as e:
			logger.error(f"Keithley resource could not be acquired at address '{self.address}': {e}.")
			raise

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		if self.resource:
			try:
				self.resource.write(":output off")
			except visa.VisaIOError as e:
				logger.error(f"Error turning off Keithley output during exit: {e}.")
			finally:
				self.resource.close()
			logger.info(f"Released Keithley at address {self.address}.")


class K2400Controller(SourcemeterController):
	def __init__(self, resource: Optional[MessageBasedResource], voltage_protection: float, current_compliance: float):
		self.max_voltage: float = 6  # max needed for 5-cell
		self.max_current: float = 0.288  # max needed for 5-cell
		self._voltage_protection: float
		self._current_compliance: float

		self.reset()
		self.set_voltage_protection(voltage_protection)
		self.set_current_compliance(current_compliance)

	def reset(self):
		self.resource.write("*RST")
		self.resource.write(":trace:clear")

	def set_voltage_protection(self, voltage_protection: float):
		self.voltage_protection = voltage_protection

	@property
	def voltage_protection(self):
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
		self.resource.write(":format:elements voltage,current,time")

	def set_sm_output(self, output: sourcemeterOutput, value: float, mode: sourcemeterMode):
		self.resource.write(f":source:function {output.value}")
		self.resource.write(f":source:{output.value}:mode {mode.value}")
		self.resource.write(f":source:{output.value} {value}")

	def read_output(self) -> List[float]:
		return [1.0]  # placeholder

	def find_open_circuit_voltage(self) -> float:
		return 1.0  # placeholder

	def jv_sweep(self, max_voltage: float, sweep_direction: sweepDirection):
		pass
