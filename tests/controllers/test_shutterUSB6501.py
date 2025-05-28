import pytest
import logging

from unittest.mock import MagicMock, patch

from nidaqmx import Task  # type: ignore


from controllers.shutterUSB6501 import shutterUSB6501

# !----------------------------Issue with patching NIDAQMX Task----------------------------!


@pytest.fixture
def mock_nidaqmx_task():
	with patch("controllers.shutterUSB6501.Task") as mock_task:
		mock_task_instance = MagicMock(spec=Task)

		mock_task.return_value = mock_task_instance
		mock_task_instance.do_channels = MagicMock()
		mock_task_instance.do_channels.add_do_chan = MagicMock()

		mock_task.return_value = mock_task_instance

		yield mock_task_instance


# Test __init__():


def test_shutter_initialises():
	shutter = shutterUSB6501(output_channel="Testboard/port1/line0", enabled=True)
	assert shutter.enabled is True
	assert shutter.output_channel == "Testboard/port1/line0"
	assert shutter.task is None

	shutter_disabled = shutterUSB6501(enabled=False)
	assert shutter_disabled.enabled is False
	assert shutter_disabled.task is None


# Test __enter__():


def test_shutter_opens_if_control_enabled(caplog: pytest.LogCaptureFixture, mock_nidaqmx_task: MagicMock) -> None:
	channel = "Dev1/port0/line0"
	caplog.set_level(logging.INFO)

	with shutterUSB6501(output_channel=channel, enabled=True):
		pass

	assert caplog.records[0].message == "Shutter opened."


def test_shutterUSB6501_enter_handles_DaqError(caplog: pytest.LogCaptureFixture, mock_nidaqmx_task: MagicMock) -> None:
	pass


def test_shutter_disabled_prints_correct_message():
	pass


# Test __exit__():
