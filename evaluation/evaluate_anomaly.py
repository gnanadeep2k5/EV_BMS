import os
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def evaluate_anomaly_detection():
    """
    Evaluate Isolation Forest anomaly detection using
    the known controlled fault scenario as ground truth.
    """

    input_file = "outputs/results/anomaly_detection_results.csv"

    # Load results
    df = pd.read_csv(input_file)

    # -----------------------------------------
    # Create ground truth labels
    #
    # 0 = Normal
    # 1 = Anomaly
    #
    # Cell 3 at Time >= 80 is the controlled fault.
    # -----------------------------------------

    df["True Label"] = (
        (df["Cell"] == 3) &
        (df["Time (s)"] >= 80)
    ).astype(int)

    # Convert model predictions
    # Isolation Forest:
    # -1 = Anomaly
    #  1 = Normal

    df["Predicted Label"] = (
        df["Anomaly Prediction"] == -1
    ).astype(int)

    # -----------------------------------------
    # Calculate metrics
    # -----------------------------------------

    precision = precision_score(
        df["True Label"],
        df["Predicted Label"],
        zero_division=0
    )

    recall = recall_score(
        df["True Label"],
        df["Predicted Label"],
        zero_division=0
    )

    f1 = f1_score(
        df["True Label"],
        df["Predicted Label"],
        zero_division=0
    )

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(
        df["True Label"],
        df["Predicted Label"]
    ).ravel()

    # False Alarm Rate
    false_alarm_rate = fp / (fp + tn) if (fp + tn) > 0 else 0

    # -----------------------------------------
    # Detection delay
    # -----------------------------------------

    fault_start_time = 80

    detected_fault_rows = df[
        (df["True Label"] == 1) &
        (df["Predicted Label"] == 1)
    ]

    if not detected_fault_rows.empty:

        first_detection_time = detected_fault_rows[
            "Time (s)"
        ].min()

        detection_delay = (
            first_detection_time - fault_start_time
        )

    else:
        first_detection_time = None
        detection_delay = None

    # -----------------------------------------
    # Display results
    # -----------------------------------------

    print("\nANOMALY DETECTION EVALUATION")
    print("-" * 40)

    print(f"Precision        : {precision:.4f}")
    print(f"Recall           : {recall:.4f}")
    print(f"F1-Score         : {f1:.4f}")
    print(f"False Alarm Rate : {false_alarm_rate:.4f}")

    print("\nConfusion Matrix")
    print(f"True Negatives  : {tn}")
    print(f"False Positives : {fp}")
    print(f"False Negatives : {fn}")
    print(f"True Positives  : {tp}")

    print(f"\nFault Start Time      : {fault_start_time} seconds")

    if first_detection_time is not None:
        print(
            f"First Detection Time  : "
            f"{first_detection_time} seconds"
        )

        print(
            f"Detection Delay       : "
            f"{detection_delay} seconds"
        )
    else:
        print("No fault anomaly was detected.")

    # -----------------------------------------
    # Save evaluation summary
    # -----------------------------------------

    os.makedirs("outputs/results", exist_ok=True)

    summary = pd.DataFrame({
        "Metric": [
            "Precision",
            "Recall",
            "F1-Score",
            "False Alarm Rate",
            "True Negatives",
            "False Positives",
            "False Negatives",
            "True Positives",
            "Fault Start Time",
            "First Detection Time",
            "Detection Delay"
        ],
        "Value": [
            precision,
            recall,
            f1,
            false_alarm_rate,
            tn,
            fp,
            fn,
            tp,
            fault_start_time,
            first_detection_time,
            detection_delay
        ]
    })

    output_file = "outputs/results/anomaly_evaluation.csv"

    summary.to_csv(output_file, index=False)

    print(f"\nEvaluation saved to: {output_file}")


if __name__ == "__main__":
    evaluate_anomaly_detection()