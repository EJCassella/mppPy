import numpy as np
from numpy.typing import NDArray


def calc_mpp_from_iv(iv_data_array: NDArray[np.float64]) -> float:
	# iv_data_array must be n * 2 array of current (I) and voltage (V) data
	i = iv_data_array[:, 0]
	v = iv_data_array[:, 1]
	p = abs(v * i)
	mpp_ind = np.argmax(p)
	Vmpp = v[mpp_ind]
	return Vmpp
