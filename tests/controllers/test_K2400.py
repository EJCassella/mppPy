import pytest
import pyvisa as visa
import logging

from unittest.mock import MagicMock, patch

from pyvisa.resources import GPIBInstrument

from controllers.K2400 import K2400Context


@pytest.fixture
def mock_sys_exit():
	with patch("sys.exit") as mock_exit:
		yield mock_exit


@pytest.fixture
def mock_pyvisa_resource_manager():
	with patch("pyvisa.ResourceManager") as mockRM:
		mock_K2400GPIB = MagicMock(spec=GPIBInstrument)
		mockRM.return_value.open_resource.return_value = mock_K2400GPIB
		yield mock_K2400GPIB


# Testing __init__()


def test_K2400context_initialises_with_address():
	sm = K2400Context("20")
	assert sm.address == "GPIB0::20::INSTR"
	assert sm.resource is None


def test_K2400context_init_raises_value_error_mising_address():
	with pytest.raises(ValueError, match="Keithley GPIB connection could not be initiated"):
		K2400Context("")


# Testing __enter__()


def test_K2400context_enter_acquires_resource(
	caplog: pytest.LogCaptureFixture, mock_pyvisa_resource_manager: MagicMock
) -> None:
	address = "20"
	expected_gpib_address = f"GPIB0::{address}::INSTR"
	caplog.set_level(logging.INFO)
	with K2400Context(address) as instrument:
		visa.ResourceManager.assert_called_once()  # type: ignore
		visa.ResourceManager.return_value.open_resource.assert_called_once_with(  # type: ignore
			resource_name=expected_gpib_address, timeout=60000, _read_termination="\n"
		)
		assert instrument is mock_pyvisa_resource_manager
		assert caplog.records[0].message == f"Keithley acquired at address {expected_gpib_address}."


def test_K2400context_enter_handles_VISAIOerror(
	caplog: pytest.LogCaptureFixture, mock_pyvisa_resource_manager: MagicMock, mock_sys_exit: MagicMock
):
	address = "99"
	expected_gpib_address = f"GPIB0::{address}::INSTR"

	simulated_error_code = -1073807343  # VI_ERROR_RSRC_NFOUND
	mock_visa_error = visa.VisaIOError(simulated_error_code)

	visa.ResourceManager.return_value.open_resource.side_effect = mock_visa_error  # type: ignore
	expected_error_message = f"Keithley resource could not be acquired at address '{expected_gpib_address}'"

	caplog.set_level(logging.ERROR)

	with K2400Context(address):
		pass

	assert expected_error_message in caplog.records[0].message


# Testing __exit__()


def test_K2400context_exit_releases_resource_and_logs():
	pass


def test_K2400context_exit_releases_on_exception():
	pass


def test_K2400context_exit_handles_error_during_shutdown():
	pass
