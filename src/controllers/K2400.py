import pyvisa as visa
import sys

from typing import Optional, cast
from types import TracebackType

from controllers.interfaces import SourcemeterContext, SourcemeterController, sourcemeterOutput, sweepDirection

from utils.logger_config import setup_logger

from pyvisa.resources import GPIBInstrument

logger = setup_logger()


class K2400Context(SourcemeterContext):
	resource: Optional[GPIBInstrument]

	def __init__(self, address: Optional[str]):
		if address:
			self.address = "GPIB0::" + address + "::INSTR"
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
			sys.exit(1)

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
	def set_current_compliance(self, current_compliance: float):
		pass

	def set_voltage_protection(self, voltage_protection: float):
		pass

	def configure_data_output(self):
		pass

	def set_sm_output(self, output: sourcemeterOutput):
		pass

	def read_current_voltage_time(self):
		pass

	def find_open_circuit_voltage(self):
		pass

	def jv_sweep(self, start_voltage: float, end_voltage: float, sweep_direction: sweepDirection):
		pass
