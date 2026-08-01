from simulation.battery_cell import BatteryCell
from simulation.export_data import save_to_csv
from simulation.fault_injection import inject_fault


def run_simulation():

    print("\nStarting Battery Simulation...\n")

    # Create four healthy cells
    battery_pack = [BatteryCell(i) for i in range(1, 5)]

    simulation_data = []

    simulation_time = 200

    for time_step in range(simulation_time):

        for cell in battery_pack:

            # Update battery state
            cell.update()

            # Fault injection (currently empty)
            inject_fault(cell, time_step)

            # Store battery state
            simulation_data.append(
                cell.get_state(time_step)
            )

    df = save_to_csv(simulation_data)

    print("\nSimulation completed successfully!\n")

    print(df.head())


if __name__ == "__main__":
    run_simulation()