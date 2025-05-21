import pytest
import logging

from controllers.dummyShutter import dummyShutter


# Test __enter__():
def test_shutter_opens_if_enabled(caplog: pytest.LogCaptureFixture):
	caplog.set_level(logging.INFO)

	with dummyShutter(enabled=True):
		pass

	assert caplog.records[0].message == "Shutter opened."


# Test __exit__():
