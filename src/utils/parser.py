import argparse


def parse_arguments(args: list[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Maximum power point tracking for PV devices using GPIB connected sourcemeter and optional shutter control."
	)

	parser.add_argument("tracking_time_seconds", type=int, help="Total number of seconds to MPP track for.")
	parser.add_argument("device_area_cm2", type=float, help="Device active area in cm^2.")
	parser.add_argument("-g", "--gpib_address", default="20", type=str, help="GPIB address number for sourcemeter.")
	parser.add_argument(
		"-s",
		"--shutter",
		default=False,
		action="store_true",
		help="Optional flag for shutter control.",
	)

	return parser.parse_args(args)
