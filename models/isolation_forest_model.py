import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def train_and_detect_anomalies():
    """
    Train Isolation Forest only on healthy battery behaviour
    and detect anomalies in the complete dataset.
    """

    input_file = "data/processed/ml_ready_data.csv"

    # Load ML-ready dataset
    df = pd.read_csv(input_file)

    # -----------------------------------------
    # Features used for anomaly detection
    # -----------------------------------------

    feature_columns = [
        "Voltage (V)",
        "Temperature (°C)",
        "Temperature Difference (°C)",
        "Temperature Rate (°C/s)",
        "Voltage Deviation (V)",
        "Internal Resistance (Ω)",
        "Resistance Deviation (Ω)"
    ]

    # -----------------------------------------
    # Create healthy training dataset
    #
    # Cells 1, 2 and 4 are always healthy.
    # Cell 3 is healthy only before Time = 80.
    # -----------------------------------------

    healthy_data = df[
        (df["Cell"].isin([1, 2, 4])) |
        (
            (df["Cell"] == 3) &
            (df["Time (s)"] < 80)
        )
    ].copy()

    X_train = healthy_data[feature_columns]

    # Complete dataset for anomaly detection
    X_test = df[feature_columns]

    # -----------------------------------------
    # Scale using ONLY healthy training data
    # -----------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # -----------------------------------------
    # Train Isolation Forest
    # -----------------------------------------

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X_train_scaled)

    # -----------------------------------------
    # Detect anomalies in complete dataset
    #
    #  1  = Normal
    # -1  = Anomaly
    # -----------------------------------------

    predictions = model.predict(X_test_scaled)

    # Lower score = more anomalous
    anomaly_scores = model.decision_function(X_test_scaled)

    # Add results
    df["Anomaly Prediction"] = predictions
    df["Anomaly Score"] = anomaly_scores

    df["Status"] = df["Anomaly Prediction"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # -----------------------------------------
    # Create output folders
    # -----------------------------------------

    os.makedirs("outputs/models", exist_ok=True)
    os.makedirs("outputs/results", exist_ok=True)

    # Save trained model and scaler
    joblib.dump(
        model,
        "outputs/models/isolation_forest.joblib"
    )

    joblib.dump(
        scaler,
        "outputs/models/isolation_forest_scaler.joblib"
    )

    # Save results
    output_file = "outputs/results/anomaly_detection_results.csv"

    df.to_csv(output_file, index=False)

    # -----------------------------------------
    # Display results
    # -----------------------------------------

    print("\nIsolation Forest completed successfully!")

    print("\nHealthy training records:", len(healthy_data))
    print("Total records tested:", len(df))

    print("\nOverall anomaly counts:")
    print(df["Status"].value_counts())

    print("\nAnomalies detected by cell:")
    print(
        df[df["Status"] == "Anomaly"]
        .groupby("Cell")
        .size()
    )

    # Check Cell 3 specifically after fault begins
    cell_3_after_fault = df[
        (df["Cell"] == 3) &
        (df["Time (s)"] >= 80)
    ]

    print("\nCell 3 anomaly counts after fault begins:")
    print(cell_3_after_fault["Status"].value_counts())

    # Find first detected anomaly in Cell 3
    detected_anomalies = cell_3_after_fault[
        cell_3_after_fault["Status"] == "Anomaly"
    ]

    if not detected_anomalies.empty:

        first_detection_time = detected_anomalies[
            "Time (s)"
        ].iloc[0]

        print(
            f"\nFirst Cell 3 anomaly detected at "
            f"Time = {first_detection_time} seconds"
        )

        detection_delay = first_detection_time - 80

        print(
            f"Detection delay = {detection_delay} seconds"
        )

    else:
        print("\nNo Cell 3 anomaly was detected after the fault.")

    print("\nLast 10 records for Cell 3:")

    print(
        df[df["Cell"] == 3][
            [
                "Time (s)",
                "Temperature (°C)",
                "Temperature Difference (°C)",
                "Internal Resistance (Ω)",
                "Resistance Deviation (Ω)",
                "Anomaly Score",
                "Status"
            ]
        ].tail(10)
    )

    print(f"\nResults saved to: {output_file}")

    return df


if __name__ == "__main__":
    train_and_detect_anomalies()