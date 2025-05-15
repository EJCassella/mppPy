import re

from pydantic import BaseModel, Field, field_validator

VALID_GPIB_ADDRESS_REGEX = re.compile(r"^[0-9]{1,2}$")


class UserSetting(BaseModel):
	tracking_time_seconds: int = Field(gt=0)
	device_area_cm2: float = Field(gt=0)
	gpib_address: str
	shutter: bool

	@field_validator("gpib_address", mode="after")
	@classmethod
	def validate_tracking_time(cls, v: str | None) -> str | None:
		if v:
			if not VALID_GPIB_ADDRESS_REGEX.match(v):
				raise ValueError(
					f"GPIB address '{v}' is invalid. Should be a two digit number, typically between 0 and 30."
				)
		return v
