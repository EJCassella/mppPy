import argparse


def parse_arguments(args: list[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Maximum power point tracking for PV devices using GPIB connected sourcemeter and optional shutter control."
	)

	parser.add_argument("tracking_time_seconds", type=int, help="Total number of seconds to MPP track for.")
	parser.add_argument("device_area_cm2", type=float, help="Device active area in cm^2.")
	parser.add_argument(
		"-g",
		"--gpib_address",
		default="20",
		type=str,
		help="GPIB address number for sourcemeter. Expecting number for address, typically an integer between 0 and 30. e.g. -g 20",
	)
	parser.add_argument(
		"-s",
		"--shutter",
		default=False,
		action="store_true",
		help="Optional flag for shutter control.",
	)
	parser.add_argument(
		"-d",
		"--dummyMode",
		default=False,
		action="store_true",
		help="Optional flag to run mppPy in dummy mode.",
	)
	parser.add_argument(
		"-m",
		"--metadata",
		type=str,
		help="Add metadata to data outputs, e.g. -m Device21_triple_cat_spin",
	)

	return parser.parse_args(args)
