# type: ignore
import time
import numpy as np

from typing import Sequence, Any

from controllers.interfaces import SourcemeterController, sweepDirection, sourcemeterOutput, sourcemeterMode

# from utils.determine_vmpp import determine_mpp
# from utils.custom_exceptions import OutputLimitsExceededError
from utils.logger_config import setup_logger
from utils.constants import SWEEP_RATE

logger = setup_logger()


class MaximumPowerPointTracker:
	def __init__(
		self,
		sourcemeter: SourcemeterController,
		cell_area: float,
		tracking_time: int,
		dummyMode: bool,
	):
		self.dummyMode: bool = dummyMode
		self.sm: SourcemeterController = sourcemeter
		self.cell_area: float = cell_area
		self.tracking_time: int = tracking_time

	def find_open_circuit_voltage(self, hold_time: int = 5) -> float:
		self.sm.set_sm_output(output=sourcemeterOutput.CURRENT, value=0, mode=sourcemeterMode.FIXED)
		logger.info(
			f"Holding device at 0 applied current for {hold_time} seconds before measuring open circuit voltage."
		)
		time.sleep(hold_time)
		logger.info("Measuring open circuit voltage...")
		_, Voc, _ = self.sm.read_output()
		logger.info(f"Device Voc measured as {Voc} V.")
		self.sm.output_off()
		return Voc

	def jv_sweep(self, max_voltage: float, sweep_direction: sweepDirection) -> Sequence[Any]:
		if sweep_direction != sweepDirection.BOTH:
			self.sm.set_sm_output(
				output=sourcemeterOutput.VOLTAGE,
				value=max_voltage,
				mode=sourcemeterMode.SWEEP,
				sweepdir=sweep_direction,
			)
			i, v, _ = self.sm.read_output()
			self.sm.output_off()
			return [i, v]

		else:
			self.sm.set_sm_output(
				output=sourcemeterOutput.VOLTAGE,
				value=max_voltage,
				mode=sourcemeterMode.SWEEP,
				sweepdir=sweepDirection.FORWARD,
			)
			iFwd, vFwd, _ = self.sm.read_output()

			self.sm.set_sm_output(
				output=sourcemeterOutput.VOLTAGE,
				value=max_voltage,
				mode=sourcemeterMode.SWEEP,
				sweepdir=sweepDirection.REVERSE,
			)
			iBcwd, vBcwd, _ = self.sm.read_output()
			# TO DO: return proxy JV array for MPP calculation

			self.sm.output_off()
			return [iFwd, iBcwd, vFwd, vBcwd]

	@property
	def nPoints(self):
		return self._npoints

	@nPoints.setter
	def nPoints(self, Voc: float):
		self._nPoints = Voc / (0.05 * SWEEP_RATE)  # voltage (V) / (delay (S) * sweep_rate (V/s))

	def find_initial_vmpp(self):
		Voc = self.find_open_circuit_voltage()
		jv_sweep = self.jv_sweep(
			max_voltage=Voc,
			sweep_direction=sweepDirection.REVERSE,
		)
		jv_sweep = np.reshape(jv_sweep, (-1, 2))

		# self.initial_vmpp = determine_mpp(
		# 	jv_data
		# )

		return self.initial_vmpp

	# !--------------------- UNFISNISHED IMPLEMENTATIONS BELOW -----------------------------!

	# def walk_to_initial_vmpp(self):
	# 	Vset = 0
	# 	while Vset < self._initial_vmpp:
	# 		self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE)  # set to output voltage at vmpp
	# 		Vset += self._vstep

	# def run(self):
	# 	self.find_initial_vmpp()
	# 	self.walk_to_initial_vmpp()
	# 	i, v, t0 = self.read_output()
	# 	self._start_time = t0

	# 	previous_power = abs(v * i)
	# 	direction = 1

	# 	try:
	# 		while True:
	# 			self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE, value=self.vmpp)
	# 			i, v, tx = self._sm.read_output()
	# 			power = abs(v * i)

	# 			self.check_runtime(tx)
	# 			self.update_plot(i, v, tx)

	# 			if power > previous_power:
	# 				self.Vmpp += direction * self.v_step
	# 			else:
	# 				direction *= -1
	# 				self.Vmpp += direction * self.v_step

	# 			previous_power = power
	# 	except KeyboardInterrupt:
	# 		pass
	# 	except OutputLimitsExceededError:  # if something is running away
	# 		pass
	# 	finally:
	# 		# set output to 0 should be handled by context manager but just as fail safe
	# 		self.sm.set_sm_output(output=sourcemeterOutput.VOLTAGE, value=0, mode=sourcemeterMode.FIXED)
	# 		logger.info("Tracking finished.")
