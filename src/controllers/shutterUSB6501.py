from utils.logger_config import setup_logger
from controllers.interfaces import ShutterContext
from types import TracebackType
from nidaqmx import Task  # type: ignore
from nidaqmx.errors import DaqError  # type: ignore
from typing import Optional

logger = setup_logger()


class shutterUSB6501(ShutterContext):
	def __init__(self, output_channel: str = "Testboard/port1/line0", enabled: bool = True) -> None:
		self.output_channel = output_channel
		self.enabled = enabled
		self.task: Optional[Task] = None  # type: ignore

	def __enter__(self) -> Optional[Task]:
		if self.enabled:
			try:
				self.task = Task()
				self.task.do_channels.add_do_chan(self.output_channel)  # type: ignore
				self.task.start()  # type: ignore
				self.task.write([False])  # type: ignore - Initialise shutter state OPEN
				logger.info("Shutter opened.")
				return self.task  # type: ignore
			except DaqError as e:
				logger.error(f"Error communicating with shutter at channel {self.output_channel}: {e}.")
				raise
		else:
			logger.info("Shutter control is disabled.")

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		if self.task:  # type: ignore
			try:
				logger.info(f"Closed shutter control at {self.output_channel}.")
				self.task.write([True])  # type: ignore - Set shutter state CLOSED
				self.task.stop()  # type: ignore
				self.task.close()  # type: ignore
			except DaqError as e:
				logger.error(f"Error releasing shutter control: {e}")
