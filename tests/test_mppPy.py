import pytest

from mppPy import sample_func


@pytest.mark.parametrize("int1, int2, expected", [(2, 7, 9), (1, 3, 4), (1, 1, 2), (-1, 3, 2)])
def test_sample_func(int1: int, int2: int, expected: int) -> None:
	assert sample_func(int1, int2) == expected
