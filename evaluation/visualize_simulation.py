import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_simulation():

    # Load simulation data
    filepath = "data/simulation_output.csv"
    df = pd.read_csv(filepath)

    # Create output folder
    os.makedirs("outputs/graphs", exist_ok=True)

    # Create one window with 3 graphs
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # ---------------------------------
    # 1. Temperature vs Time
    # ---------------------------------
    for cell in sorted(df["Cell"].unique()):

        cell_data = df[df["Cell"] == cell]

        axes[0].plot(
            cell_data["Time (s)"],
            cell_data["Temperature (°C)"],
            label=f"Cell {cell}"
        )

    axes[0].set_title(
        "Temperature vs Time",
        loc="left",
        pad=15
    )
    axes[0].set_xlabel("Time (s)", labelpad=10)
    axes[0].set_ylabel("Temperature (°C)", labelpad=10)
    axes[0].legend()
    axes[0].grid(True)

    # ---------------------------------
    # 2. Voltage vs Time
    # ---------------------------------
    for cell in sorted(df["Cell"].unique()):

        cell_data = df[df["Cell"] == cell]

        axes[1].plot(
            cell_data["Time (s)"],
            cell_data["Voltage (V)"],
            label=f"Cell {cell}"
        )

    axes[1].set_title(
        "Voltage vs Time",
        loc="left",
        pad=15
    )
    axes[1].set_xlabel("Time (s)", labelpad=10)
    axes[1].set_ylabel("Voltage (V)", labelpad=10)
    axes[1].legend()
    axes[1].grid(True)

    # ---------------------------------
    # 3. Internal Resistance vs Time
    # ---------------------------------
    for cell in sorted(df["Cell"].unique()):

        cell_data = df[df["Cell"] == cell]

        axes[2].plot(
            cell_data["Time (s)"],
            cell_data["Internal Resistance (Ω)"],
            label=f"Cell {cell}"
        )

    axes[2].set_title(
        "Internal Resistance vs Time",
        loc="left",
        pad=15
    )
    axes[2].set_xlabel("Time (s)", labelpad=10)
    axes[2].set_ylabel("Internal Resistance (Ω)", labelpad=10)
    axes[2].legend()
    axes[2].grid(True)

    # Space between graphs
    fig.subplots_adjust(hspace=0.45)

    # Save combined graph
    plt.savefig(
        "outputs/graphs/simulation_analysis.png",
        dpi=300,
        bbox_inches="tight"
    )

    # Show all graphs
    plt.show()


if __name__ == "__main__":
    plot_simulation()