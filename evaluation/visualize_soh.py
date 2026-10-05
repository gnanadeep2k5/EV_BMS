import pandas as pd
import matplotlib.pyplot as plt
import os


def visualize_soh():

    # Load processed NASA data
    file_path = "data/processed/NASA_B0006_SoH.csv"
    df = pd.read_csv(file_path)

    # Create graph
    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Cycle"],
        df["SoH (%)"],
        marker="o",
        markersize=3
    )

    plt.xlabel("Discharge Cycle")
    plt.ylabel("State of Health (%)")
    plt.title("NASA B0006 Battery State of Health")

    plt.grid(True)

    # Save graph
    os.makedirs("outputs/graphs", exist_ok=True)

    output_file = "outputs/graphs/nasa_b0006_soh.png"

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"SoH graph saved to: {output_file}")

    plt.show()


if __name__ == "__main__":
    visualize_soh()