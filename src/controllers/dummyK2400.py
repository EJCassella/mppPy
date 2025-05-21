import pyvisa as visa
import sys

from typing import Optional
from types import TracebackType

from controllers.interfaces import SourcemeterContext

from utils.logger_config import setup_logger

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

	def __enter__(self) -> None:
		logger.info(f"Keithley acquired at address {self.address}.")

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		logger.info(f"Released Keithley at address {self.address}.")
