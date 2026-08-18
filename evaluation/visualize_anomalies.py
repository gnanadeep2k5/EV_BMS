import os
import pandas as pd
import matplotlib.pyplot as plt


def visualize_anomalies():
    """
    Visualize battery temperature and highlight
    records detected as anomalies by Isolation Forest.
    """

    input_file = "outputs/results/anomaly_detection_results.csv"

    # Load anomaly detection results
    df = pd.read_csv(input_file)

    # Create graph output folder
    os.makedirs("outputs/graphs", exist_ok=True)

    # Create graph
    plt.figure(figsize=(12, 7))

    # Plot temperature for all cells
    for cell in sorted(df["Cell"].unique()):

        cell_data = df[df["Cell"] == cell]

        plt.plot(
            cell_data["Time (s)"],
            cell_data["Temperature (°C)"],
            label=f"Cell {cell}"
        )

    # Get anomaly records
    anomalies = df[df["Status"] == "Anomaly"]

    # Mark anomalies
    plt.scatter(
        anomalies["Time (s)"],
        anomalies["Temperature (°C)"],
        marker="x",
        s=60,
        label="Detected Anomaly"
    )

    # Mark fault injection time
    plt.axvline(
        x=80,
        linestyle="--",
        label="Fault Injection Starts"
    )

    # Labels
    plt.title(
        "Battery Thermal Anomaly Detection",
        loc="left",
        pad=15
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    # Save graph
    output_file = "outputs/graphs/anomaly_detection.png"

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"\nGraph saved successfully to: {output_file}")

    plt.show()


if __name__ == "__main__":
    visualize_anomalies()