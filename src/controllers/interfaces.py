import pyvisa as visa

from abc import ABC, abstractmethod
from enum import Enum
from types import TracebackType


class sourcemeterOutput(Enum):
	CURRENT = 1
	VOLTAGE = 2


class sweepDirection(Enum):
	FORWARD = 1
	REVERSE = 2
	BOTH = 3


class SourcemeterContext(ABC):
	@abstractmethod
	def __init__(self, address: str):
		self.address = address
		self.resource = None

	@abstractmethod
	def __enter__(self) -> visa.resources.Resource | None:
		pass

	@abstractmethod
	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		pass


class SourcemeterController(ABC):
	@abstractmethod
	def __init__(self, address: str):
		self.address = address
		self.resource = None

	@abstractmethod
	def set_current_compliance(self, current_compliance: float):
		pass

	@abstractmethod
	def set_voltage_protection(self, voltage_protection: float):
		pass

	@abstractmethod
	def configure_data_output(self):
		pass

	@abstractmethod
	def set_sm_output(self, output: sourcemeterOutput):
		pass

	@abstractmethod
	def read_current_voltage_time(self):
		pass

	@abstractmethod
	def find_open_circuit_voltage(self):
		pass

	@abstractmethod
	def jv_sweep(self, start_voltage: float, end_voltage: float, sweep_direction: sweepDirection):
		pass


class ShutterContext(ABC):
	@abstractmethod
	def __enter__(self):
		pass

	@abstractmethod
	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	):
		pass
