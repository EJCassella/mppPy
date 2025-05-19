import pytest

from utils.validator import UserSetting
from pydantic import ValidationError


@pytest.mark.parametrize(
	"tracking_time_seconds, device_area_cm2,	gpib_address, shutter",
	[
		(0, 0, "20", False),
		(-1, 1, "20", False),
		(1, -1, "20", False),
		(10, 1, "101", False),
		(10, 1, "abc", False),
		(10, 1, "x99", False),
		(10, 1, "None", False),
	],
)
def test_user_setting_validation_fails_with_invalid_entries(
	tracking_time_seconds: int,
	device_area_cm2: float,
	gpib_address: str | None,
	shutter: bool,
) -> None:
	with pytest.raises(ValidationError):
		UserSetting(
			tracking_time_seconds=tracking_time_seconds,
			device_area_cm2=device_area_cm2,
			gpib_address=gpib_address,
			shutter=shutter,
		)
