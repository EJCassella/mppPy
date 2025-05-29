from abc import ABC, abstractmethod
from enum import Enum
from types import TracebackType

from pyvisa.resources import MessageBasedResource
from typing import Optional, Sequence, Any

from nidaqmx import Task  # type: ignore


class sourcemeterOutput(Enum):
	CURRENT = "current"
	VOLTAGE = "voltage"


class sweepDirection(Enum):
	FORWARD = "forward"
	REVERSE = "reverse"
	BOTH = "both"


class sourcemeterMode(Enum):
	FIXED = "fixed"
	SWEEP = "sweep"
	LIST = "list"


class SourcemeterContext(ABC):
	@abstractmethod
	def __init__(self, address: str) -> None:
		self.address = address
		self.resource = None

	@abstractmethod
	def __enter__(self) -> MessageBasedResource:
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
	def __init__(self, resource: MessageBasedResource, voltage_protection: float, current_compliance: float):
		self.resource: MessageBasedResource = resource
		self._voltage_protection: float
		self._current_compliance: float

		self.max_voltage: float  # Absolute upper limit required in Volts
		self.max_current: float  # Absolute upper limit required in Amps

	@abstractmethod
	def reset(self):
		pass

	@property
	@abstractmethod
	def voltage_protection(self) -> float:
		pass

	@voltage_protection.setter
	@abstractmethod
	def voltage_protection(self, voltage: float):
		pass

	@abstractmethod
	def configure_data_output(self):
		pass

	@abstractmethod
	def set_sm_output(
		self,
		output: sourcemeterOutput,
		value: float,
		mode: sourcemeterMode,
		sweepdir: sweepDirection,
		sweep_rate: float,
	):
		pass

	@abstractmethod
	def read_output(self) -> Sequence[Any]:
		pass


class ShutterContext(ABC):
	@abstractmethod
	def __init__(self, enabled: bool) -> None:
		pass

	@abstractmethod
	def __enter__(self) -> Optional[Task]:
		pass

	@abstractmethod
	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		pass
