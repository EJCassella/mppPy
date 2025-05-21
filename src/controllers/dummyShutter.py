from utils.logger_config import setup_logger
from controllers.interfaces import ShutterContext
from types import TracebackType

logger = setup_logger()


class dummyShutter(ShutterContext):
	def __init__(self, enabled: bool = True) -> None:
		self.enabled = enabled
		self.task: bool

	def __enter__(self) -> None:
		if self.enabled:
			logger.info("Shutter opened.")
			self.task = True
		else:
			logger.info("Shutter control is disabled.")
			self.task = False

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		if self.task:
			logger.info("Closed shutter.")
		else:
			logger.info("Shutter control exited.")
