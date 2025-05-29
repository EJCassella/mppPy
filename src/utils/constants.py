"""For 3-cells expect 1.2V * 3 max voltage, protection set in Volts and 24 mA/cm^2 * 2.4cm^2, set in Amps. Absolute hard limits (enough for 5-cell design) set to 6.5 V and 0.288 A in K2400 class. Only change the hard limit if absolutely necessary, i.e. active areas greater than 11.5 cm^2 or more than 5 cells. Keep the protection and compliance as low as necessary for you application for safety during measurements."""

VOLTAGE_PROTECTION = 3.6
CURRENT_COMPLIANCE = 0.058
SWEEP_RATE = 0.04  # Target sweep rate in V/s for JV scans
