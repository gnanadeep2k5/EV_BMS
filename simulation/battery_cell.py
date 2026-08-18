import random


class BatteryCell:
    """
    Represents a single lithium-ion battery cell.
    """

    def __init__(self, cell_id):
        self.cell_id = cell_id

        # Electrical properties
        self.voltage = 3.70
        self.current = 2.0

        # Thermal properties
        self.temperature = 25.0

        # Battery state
        self.soc = 40.0

        # New property
        self.internal_resistance = 0.050   # Ohms

    def update(self):

        # Increase SoC
        self.soc = min(self.soc + 0.5, 100)

        # Voltage rises while charging
        self.voltage = min(
            self.voltage + random.uniform(0.001, 0.004),
            4.20
        )

        # Heat generated (simplified Joule heating)
        heat_generated = (
            (self.current ** 2)
            * self.internal_resistance
            * 0.05
        )

        # Temperature rise
        self.temperature += heat_generated + random.uniform(0.005, 0.02)

    def get_state(self, time_step):

        return {

            "Time (s)": time_step,

            "Cell": self.cell_id,

            "Voltage (V)": round(self.voltage, 3),

            "Current (A)": round(self.current, 2),

            "Temperature (°C)": round(self.temperature, 2),

            "SoC (%)": round(self.soc, 2),

            "Internal Resistance (Ω)": round(
                self.internal_resistance,
                4
            )
        }