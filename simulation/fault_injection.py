def inject_fault(cell, time_step):

    if cell.cell_id != 3:
        return

    if time_step >= 80:

        cell.internal_resistance += 0.0006
        cell.voltage -= 0.0004
        cell.temperature += 0.03