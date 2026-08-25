def inject_fault(cell, time_step):
    """
    Introduce a gradual fault
    in Cell 3.
    """

    if cell.cell_id != 3:
        return

    # Fault begins after 10 seconds

    if time_step >= 80:

        # Resistance slowly increases

        cell.internal_resistance += 0.0006

        # Voltage drops slightly because of resistance

        cell.voltage -= 0.0004

        # Extra heating

        cell.temperature += 0.03