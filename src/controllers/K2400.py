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
from utils.custom_exceptions import OutputsExceededError

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

	def __enter__(self) -> Optional[GPIBInstrument]:
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
	def __init__(self, resource: MessageBasedResource):
		self.resource: MessageBasedResource = resource
		self._voltage_protection: float = 0
		self.reset()

	def reset(self):
		self.resource.write("*RST")
		self.resource.write(":trace:clear")

	@property
	def voltage_protection(self):
		return self._voltage_protection

	@voltage_protection.setter
	def voltage_protection(self, voltage: float):
		if voltage > 5:
			self._voltage_protection = 5
			logger.warning("Trying to set voltage protection too high. Limiting voltage to 5 V.")
		elif voltage <= 0:
			self._voltage_protection = 5
			logger.warning("Trying to set voltage protection too low. Setting voltage limit to 5 V.")
		else:
			self._voltage_protection = voltage
			logger.info(f"Setting voltage limit to {voltage} V.")

	def configure_data_output(self):
		self.resource.write(":format:elements voltage,current,time")

	def set_sm_output(self, output: sourcemeterOutput, value: float, mode: sourcemeterMode):
		self.resource.write(f":source:function {output.value}")
		self.resource.write(f":source:{output.value}:mode {mode.value}")
		self.resource.write(f":source:{output.value} {value}")

	def read_output(self) -> List[float]:
		pass

	def find_open_circuit_voltage(self):
		pass

	def jv_sweep(self, start_voltage: float, end_voltage: float, sweep_direction: sweepDirection):
		pass
