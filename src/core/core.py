# type: ignore

import logging

from controllers.interfaces import SourcemeterController, sweepDirection, sourcemeterOutput

from utils.determine_vmpp import determine_mpp


class MaximumPowerPointTracker:
	def __init__(self, sourcemeter: SourcemeterController, cell_area: float, tracking_time: int, logger=logging.Logger):
		self._logger: logging.Logger = logger
		self._sm: SourcemeterController = sourcemeter
		self._cell_area: float = cell_area
		self._tracking_time: int = tracking_time
		self._npoints: int = 1000
		self._vstep: float = 0.01
		self._initial_vmpp: float = 0
		self._vmpp: float = 0
		self._start_time: float = None
		self._sm.configure_data_output()

	@property
	def npoints(self):
		return self._npoints

	def find_initial_vmpp(self):
		self._sm.configure_data_output()
		Voc = self._sm.find_open_circuit_voltage()
		self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE)  # set to output voltage to 0
		jv_data = self._sm.jv_sweep(start_voltage=Voc, end_voltage=0, sweep_direction=sweepDirection.REVERSE)
		self._initial_vmpp = determine_mpp(
			jv_data
		)  # add setter function to check this value before it's set and run away with
		return initial_vmpp

	def walk_to_initial_vmpp(self):
		Vset = 0
		while Vset < self._initial_vmpp:
			self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE)  # set to output voltage at vmpp
			Vset += self._vstep

	def run(self):
		self.find_initial_vmpp()
		self.walk_to_initial_vmpp()
		_, _, t0 = self.read_output()
		self._start_time = t0

		previous_power = abs(v * i)
		direction = 1

		try:
			while True:
				self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE)  # , self._vmpp
				v, i, tx = self._sm.read_output()
				power = abs(v * i)

				self.check_runtime(tx)
				self.update_plot(v, i, tx)

				if power > previous_power:
					self.Vmpp += direction * self.v_step
				else:
					direction *= -1
					self.Vmpp += direction * self.v_step

				previous_power = power
		except KeyboardInterrupt:
			pass
		except OutputLimitsExceededError:  # if something is running away
			pass
		finally:
			# set output to 0, should be handled by context manager but just as fail safe
			self._sm.set_sm_output(output=sourcemeterOutput.VOLTAGE)  # , 0, fixed
			pass
