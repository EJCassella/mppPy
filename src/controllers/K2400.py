from controllers.interfaces import SourcemeterContext, SourcemeterController, sourcemeterOutput, sweepDirection


class K2400Context(SourcemeterContext):
	def __init__(self, address: str):
		self.address = address
		self.resource = None

	def __enter__(self):
		pass

	def __exit__(self):
		pass


class K2400Controller(SourcemeterController):
	def set_current_compliance(self, current_compliance: float):
		pass

	def set_voltage_protection(self, voltage_protection: float):
		pass

	def configure_data_output(self):
		pass

	def set_sm_output(self, output: sourcemeterOutput):
		pass

	def read_current_voltage_time(self):
		pass

	def find_open_circuit_voltage(self):
		pass

	def jv_sweep(self, start_voltage: float, end_voltage: float, sweep_direction: sweepDirection):
		pass
