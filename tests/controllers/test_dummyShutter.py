import pytest
import logging

from controllers.dummyShutter import dummyShutter


# Test __enter__():
def test_shutter_opens_if_enabled(caplog: pytest.LogCaptureFixture):
	caplog.set_level(logging.INFO)

	with dummyShutter(enabled=True):
		pass

	assert caplog.records[0].message == "Shutter opened."


def test_shutter_does_not_open_if_disabled(caplog: pytest.LogCaptureFixture):
	caplog.set_level(logging.INFO)

	with dummyShutter(enabled=False):
		pass

	assert caplog.records[0].message == "Shutter control is disabled."


# Test __exit__():


def test_shutter_releases_resource(caplog: pytest.LogCaptureFixture):
	caplog.set_level(logging.INFO)

	with dummyShutter(enabled=True):
		pass

	assert caplog.records[-1].message == "Closed shutter."
