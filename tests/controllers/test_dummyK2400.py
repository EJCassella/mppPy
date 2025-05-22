import pytest
import logging

from controllers.dummyK2400 import dummyK2400Context


# Testing __init__()


def test_dummyK2400context_initialises_with_address():
	sm = dummyK2400Context("20")
	assert sm.address == "GPIB0::20::INSTR"
	assert sm.resource is None


def test_dummyK2400context_init_raises_value_error_mising_address():
	with pytest.raises(ValueError, match="Keithley GPIB connection could not be initiated"):
		dummyK2400Context("")


# Testing __enter__():


def test_dummyK2400context_enter_acquires_resource(caplog: pytest.LogCaptureFixture) -> None:
	address = "20"
	expected_gpib_address = f"GPIB0::{address}::INSTR"
	caplog.set_level(logging.INFO)
	with dummyK2400Context(address):
		pass

	assert caplog.records[0].message == f"Keithley acquired at address {expected_gpib_address}."


# Testing __exit__():


def test_dummyK2400context_exit_releases_resource(caplog: pytest.LogCaptureFixture) -> None:
	address = "20"
	expected_gpib_address = f"GPIB0::{address}::INSTR"
	caplog.set_level(logging.INFO)
	with dummyK2400Context(address):
		pass

	assert caplog.records[-1].message == f"Released Keithley at address {expected_gpib_address}."
