import pandas as pd
import matplotlib.pyplot as plt
import os


def visualize_soh_prediction():

    # Load final Linear Regression predictions
    file_path = "outputs/results/nasa_soh_linear_predictions.csv"

    df = pd.read_csv(file_path)

    plt.figure(figsize=(10, 5))

    # Actual SoH
    plt.plot(
        df["Cycle"],
        df["SoH (%)"],
        marker="o",
        markersize=3,
        label="Actual SoH"
    )

    # Predicted SoH
    plt.plot(
        df["Cycle"],
        df["Predicted SoH (%)"],
        marker="x",
        markersize=3,
        label="Predicted SoH"
    )

    plt.xlabel("Discharge Cycle")
    plt.ylabel("State of Health (%)")
    plt.title("NASA B0006: Actual vs Predicted SoH")

    plt.legend()
    plt.grid(True)

    # Create output folder
    os.makedirs("outputs/graphs", exist_ok=True)

    output_file = "outputs/graphs/nasa_b0006_soh_prediction.png"

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"SoH prediction graph saved to: {output_file}"
    )

    plt.show()


if __name__ == "__main__":
    visualize_soh_prediction()