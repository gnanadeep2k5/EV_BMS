import random


class BatteryCell:
    """
    Represents a single lithium-ion battery cell.
    """

    def __init__(self, cell_id):
        self.cell_id = cell_id
        self.voltage = 3.70          # Volts
        self.current = 2.0           # Amps
        self.temperature = 25.0      # °C
        self.soc = 40.0              # %

    def update(self):
        """
        Simulate one charging step.
        """

        # Increase SoC
        self.soc = min(self.soc + 0.5, 100)

        # Voltage slowly rises
        self.voltage = min(
            self.voltage + random.uniform(0.001, 0.005),
            4.20
        )

        # Small temperature increase
        self.temperature += random.uniform(0.01, 0.05)

    def get_state(self, time_step):
        """
        Return battery parameters.
        """

        return {
            "Time (s)": time_step,
            "Cell": self.cell_id,
            "Voltage (V)": round(self.voltage, 3),
            "Current (A)": round(self.current, 2),
            "Temperature (°C)": round(self.temperature, 2),
            "SoC (%)": round(self.soc, 2)
        }