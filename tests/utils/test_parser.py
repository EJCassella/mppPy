import pytest
import shlex

from utils.parser import parse_arguments


@pytest.mark.parametrize(
	"command, tracking_time_seconds, device_area_cm2, gpib_address, shutter",
	[
		# no params
		("", None, None, None, False),
		# each param
		("-t 10", 10, None, None, False),
		("-a 0.1", None, 0.1, None, False),
		("-g 20", None, None, "20", False),
		("-s", None, None, None, True),
		# all params
		("-t 10 -a 0.1 -g 20 -s", 10, 0.1, "20", True),
		# wrong param type
		# ("-t abc", None, None, None, False),
	],
)
def test_parse_arguments_accepts_valid_inputs(
	command: str, tracking_time_seconds: int, device_area_cm2: float, gpib_address: str, shutter: bool
) -> None:
	args = parse_arguments(shlex.split(command))
	assert (args.tracking_time_seconds, args.device_area_cm2, args.gpib_address, args.shutter) == (
		tracking_time_seconds,
		device_area_cm2,
		gpib_address,
		shutter,
	)


@pytest.mark.parametrize(
	"command, tracking_time_seconds, device_area_cm2, gpib_address, shutter",
	[
		("-t abc", 10, None, None, False),
		("-t 0.1", 10, None, None, False),
		("-a abc", None, 0.1, None, False),
	],
)
def test_parse_arguments_fails_with_invalid_inputs(
	command: str, tracking_time_seconds: int, device_area_cm2: float, gpib_address: str, shutter: bool
) -> None:
	with pytest.raises(SystemExit):
		parse_arguments(shlex.split(command))
