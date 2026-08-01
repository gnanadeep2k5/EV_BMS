import os
import pandas as pd


def save_to_csv(data, filename="simulation_output.csv"):

    os.makedirs("data", exist_ok=True)

    filepath = os.path.join("data", filename)

    print("Saving to:", os.path.abspath(filepath))   # <-- Add this line

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

    print(f"\nCSV saved successfully to: {filepath}")

    return df