import os
import pandas as pd


def create_features():
    """
    Load simulation data and create additional
    features for anomaly detection.
    """

    input_file = "data/simulation_output.csv"
    output_file = "data/processed/ml_ready_data.csv"

    # Load raw simulation data
    df = pd.read_csv(input_file)

    # Sort data correctly before calculating rates
    df = df.sort_values(
        by=["Cell", "Time (s)"]
    ).reset_index(drop=True)

    # -----------------------------------------
    # 1. Temperature difference from other cells
    # -----------------------------------------

    def temperature_difference(row):
        time = row["Time (s)"]
        cell = row["Cell"]

        other_cells = df[
            (df["Time (s)"] == time) &
            (df["Cell"] != cell)
        ]

        median_other_temperature = other_cells[
            "Temperature (°C)"
        ].median()

        return row["Temperature (°C)"] - median_other_temperature


    df["Temperature Difference (°C)"] = df.apply(
        temperature_difference,
        axis=1
    )

    # -----------------------------------------
    # 2. Temperature rate of rise
    # -----------------------------------------

    df["Temperature Rate (°C/s)"] = (
        df.groupby("Cell")["Temperature (°C)"]
        .diff()
        .fillna(0)
    )

    # -----------------------------------------
    # 3. Voltage deviation from other cells
    # -----------------------------------------

    def voltage_deviation(row):
        time = row["Time (s)"]
        cell = row["Cell"]

        other_cells = df[
            (df["Time (s)"] == time) &
            (df["Cell"] != cell)
        ]

        median_other_voltage = other_cells[
            "Voltage (V)"
        ].median()

        return row["Voltage (V)"] - median_other_voltage


    df["Voltage Deviation (V)"] = df.apply(
        voltage_deviation,
        axis=1
    )

    # -----------------------------------------
    # 4. Resistance deviation from other cells
    # -----------------------------------------

    def resistance_deviation(row):
        time = row["Time (s)"]
        cell = row["Cell"]

        other_cells = df[
            (df["Time (s)"] == time) &
            (df["Cell"] != cell)
        ]

        median_other_resistance = other_cells[
            "Internal Resistance (Ω)"
        ].median()

        return (
            row["Internal Resistance (Ω)"]
            - median_other_resistance
        )


    df["Resistance Deviation (Ω)"] = df.apply(
        resistance_deviation,
        axis=1
    )

    # Round calculated features
    df["Temperature Difference (°C)"] = (
        df["Temperature Difference (°C)"].round(4)
    )

    df["Temperature Rate (°C/s)"] = (
        df["Temperature Rate (°C/s)"].round(4)
    )

    df["Voltage Deviation (V)"] = (
        df["Voltage Deviation (V)"].round(4)
    )

    df["Resistance Deviation (Ω)"] = (
        df["Resistance Deviation (Ω)"].round(4)
    )

    # Create processed data folder
    os.makedirs("data/processed", exist_ok=True)

    # Save ML-ready dataset
    df.to_csv(output_file, index=False)

    print("\nFeature engineering completed successfully!")
    print(f"Processed data saved to: {output_file}")

    print("\nColumns in ML-ready dataset:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df.head(10))
    print("\nCell 3 data after fault injection:")
    
    cell_3_fault_data = df[
        (df["Cell"] == 3) &
        (df["Time (s)"] >= 80)
    ]

    print(
        cell_3_fault_data[
            [
                "Time (s)",
                "Temperature (°C)",
                "Temperature Difference (°C)",
                "Temperature Rate (°C/s)",
                "Voltage Deviation (V)",
                "Internal Resistance (Ω)",
                "Resistance Deviation (Ω)"
            ]
        ].tail(10)
    )

    return df


if __name__ == "__main__":
    create_features()