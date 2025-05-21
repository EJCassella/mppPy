import pytest

from controllers.interfaces import SourcemeterContext, SourcemeterController, ShutterContext


def test_sourcemeter_context_cannot_be_instantiated():
	with pytest.raises(TypeError):
		SourcemeterContext()  # type: ignore


def test_sourcemeter_controller_cannot_be_instantiated():
	with pytest.raises(TypeError):
		SourcemeterController()  # type: ignore


def test_shutter_context_cannot_be_instantiated():
	with pytest.raises(TypeError):
		ShutterContext()  # type: ignore
