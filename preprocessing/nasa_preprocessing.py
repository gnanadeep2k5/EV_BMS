import os
import pandas as pd
from scipy.io import loadmat


def extract_b0006_data():

    file_path = "data/nasa/B0006.mat"

    print("\nLoading NASA B0006 dataset...\n")

    # Load MATLAB file
    mat_data = loadmat(
        file_path,
        squeeze_me=True,
        struct_as_record=False
    )

    battery = mat_data["B0006"]

    records = []
    discharge_cycle = 0

    # Go through all battery cycles
    for cycle in battery.cycle:

        if cycle.type == "discharge":

            discharge_cycle += 1

            data = cycle.data

            # Extract measurements
            voltage = data.Voltage_measured
            current = data.Current_measured
            temperature = data.Temperature_measured
            time = data.Time

            capacity = float(data.Capacity)

            # Calculate simple features
            average_voltage = voltage.mean()
            average_current = abs(current).mean()
            average_temperature = temperature.mean()
            discharge_duration = time[-1] - time[0]

            records.append({
                "Cycle": discharge_cycle,
                "Average Voltage (V)": average_voltage,
                "Average Current (A)": average_current,
                "Average Temperature (°C)": average_temperature,
                "Discharge Duration (s)": discharge_duration,
                "Capacity (Ah)": capacity
            })

    # Create dataframe
    df = pd.DataFrame(records)

    # First measured capacity = reference capacity
    initial_capacity = df["Capacity (Ah)"].iloc[0]

    # Calculate SoH
    df["SoH (%)"] = (
        df["Capacity (Ah)"] / initial_capacity
    ) * 100

    # Round values
    numeric_columns = [
        "Average Voltage (V)",
        "Average Current (A)",
        "Average Temperature (°C)",
        "Discharge Duration (s)",
        "Capacity (Ah)",
        "SoH (%)"
    ]

    df[numeric_columns] = df[numeric_columns].round(4)

    # Create output directory
    os.makedirs("data/processed", exist_ok=True)

    output_file = "data/processed/NASA_B0006_SoH.csv"

    # Save CSV
    df.to_csv(output_file, index=False)

    print("NASA data processed successfully!")
    print(f"Number of discharge cycles: {len(df)}")
    print(f"Initial capacity: {initial_capacity:.4f} Ah")
    print(f"Final capacity: {df['Capacity (Ah)'].iloc[-1]:.4f} Ah")

    print("\nDataset columns:")
    print(df.columns.tolist())

    print("\nFirst 5 cycles:")
    print(df.head())

    print("\nLast 5 cycles:")
    print(df.tail())

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    extract_b0006_data()