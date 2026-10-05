from simulation.battery_cell import BatteryCell
from simulation.export_data import save_to_csv
from simulation.fault_injection import inject_fault


def run_simulation():

    print("\nStarting Battery Simulation...\n")

    battery_pack = [
        BatteryCell(i)
        for i in range(1, 5)
    ]

    simulation_data = []

    simulation_time = 200

    for time_step in range(simulation_time):

        # Store temperatures before updating cells
        previous_temperatures = {
            cell.cell_id: cell.temperature
            for cell in battery_pack
        }

        for cell in battery_pack:

            # Find immediate neighbours
            neighbour_temperatures = []

            if cell.cell_id > 1:
                neighbour_temperatures.append(
                    previous_temperatures[cell.cell_id - 1]
                )

            if cell.cell_id < len(battery_pack):
                neighbour_temperatures.append(
                    previous_temperatures[cell.cell_id + 1]
                )

            # Update cell using its neighbours
            cell.update(neighbour_temperatures)

            # Inject controlled fault
            inject_fault(cell, time_step)

            # Save state
            simulation_data.append(
                cell.get_state(time_step)
            )

    df = save_to_csv(simulation_data)

    print("\nSimulation completed successfully!\n")

    print(df.head())


if __name__ == "__main__":
    run_simulation()