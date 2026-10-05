import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI-Assisted EV BMS",
    page_icon="🔋",
    layout="wide"
)


# ==================================================
# LOAD DATA
# ==================================================

# Thermal anomaly results
anomaly_file = "outputs/results/anomaly_detection_results.csv"
anomaly_df = pd.read_csv(anomaly_file)

# Thermal evaluation metrics
evaluation_file = "outputs/results/anomaly_evaluation.csv"
evaluation_df = pd.read_csv(evaluation_file)

# NASA SoH results
soh_file = "outputs/results/nasa_soh_linear_predictions.csv"
soh_df = pd.read_csv(soh_file)


# ==================================================
# THERMAL ANOMALY ANALYSIS
# ==================================================

# Fault is intentionally introduced at 80 seconds
fault_start_time = 80

post_fault = anomaly_df[
    anomaly_df["Time (s)"] >= fault_start_time
]

# Count anomalies detected for each cell
anomaly_counts = (
    post_fault[
        post_fault["Status"] == "Anomaly"
    ]
    .groupby("Cell")
    .size()
    .sort_values(ascending=False)
)

# Cell with the highest number of detected anomalies
if len(anomaly_counts) > 0:

    detected_cell = int(anomaly_counts.index[0])

    detected_cell_data = post_fault[
        (post_fault["Cell"] == detected_cell)
        & (post_fault["Status"] == "Anomaly")
    ]

    if len(detected_cell_data) > 0:

        first_detection_time = int(
            detected_cell_data["Time (s)"].min()
        )

    else:

        first_detection_time = None

else:

    detected_cell = None
    first_detection_time = None


# Calculate detection delay
if first_detection_time is not None:

    detection_delay = (
        first_detection_time - fault_start_time
    )

else:

    detection_delay = None


# ==================================================
# EVALUATION METRICS
# ==================================================

# Read metrics from anomaly_evaluation.csv
metrics = {}

for _, row in evaluation_df.iterrows():

    metric_name = str(row.iloc[0])
    metric_value = row.iloc[1]

    metrics[metric_name] = metric_value


# Use the values from the evaluation file
precision = metrics.get("Precision")
recall = metrics.get("Recall")
f1_score = metrics.get("F1-Score")
false_alarm_rate = metrics.get("False Alarm Rate")


# ==================================================
# NASA SoH
# ==================================================

# Latest predicted SoH
latest_soh = float(
    soh_df.iloc[-1]["Predicted SoH (%)"]
)

# Latest NASA test cycle
latest_cycle = int(
    soh_df.iloc[-1]["Cycle"]
)

# SoH classification
if latest_soh >= 80:

    soh_status = "HEALTHY"

elif latest_soh >= 60:

    soh_status = "DEGRADED"

else:

    soh_status = "LOW"


# NASA model performance
soh_mae = 0.4913
soh_rmse = 0.6571


# ==================================================
# DASHBOARD TITLE
# ==================================================

st.title("AI-Assisted EV Battery Management System")

st.write(
    "Simulation-based thermal anomaly detection "
    "combined with NASA battery State-of-Health estimation."
)


# ==================================================
# SECTION 1
# THERMAL ANOMALY DETECTION
# ==================================================

st.header("1. Simulation-Based Thermal Anomaly Detection")

st.write(
    "Four-cell battery simulation with thermal coupling "
    "and a controlled fault introduced in Cell 3 at 80 seconds."
)


# --------------------------------------------------
# Main thermal metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    if detected_cell is not None:

        st.metric(
            "Detected Cell",
            f"Cell {detected_cell}"
        )

    else:

        st.metric(
            "Detected Cell",
            "None"
        )


with col2:

    st.metric(
        "Fault Start",
        f"{fault_start_time} s"
    )


with col3:

    if first_detection_time is not None:

        st.metric(
            "First Detection",
            f"{first_detection_time} s"
        )

    else:

        st.metric(
            "First Detection",
            "Not detected"
        )


with col4:

    if detection_delay is not None:

        st.metric(
            "Detection Delay",
            f"{detection_delay} s"
        )

    else:

        st.metric(
            "Detection Delay",
            "N/A"
        )


# --------------------------------------------------
# Thermal status
# --------------------------------------------------

if detected_cell is not None:

    st.warning(
        f"Thermal anomaly detected predominantly "
        f"in Cell {detected_cell}."
    )

else:

    st.success(
        "No thermal anomaly detected."
    )


# --------------------------------------------------
# Thermal model performance
# --------------------------------------------------

st.subheader("Isolation Forest Performance")

col1, col2, col3, col4 = st.columns(4)


with col1:

    if precision is not None:

        st.metric(
            "Precision",
            f"{float(precision) * 100:.1f}%"
        )

    else:

        st.metric(
            "Precision",
            "N/A"
        )


with col2:

    if recall is not None:

        st.metric(
            "Recall",
            f"{float(recall) * 100:.1f}%"
        )

    else:

        st.metric(
            "Recall",
            "N/A"
        )


with col3:

    if f1_score is not None:

        st.metric(
            "F1-Score",
            f"{float(f1_score) * 100:.1f}%"
        )

    else:

        st.metric(
            "F1-Score",
            "N/A"
        )


with col4:

    if false_alarm_rate is not None:

        st.metric(
            "False Alarm Rate",
            f"{float(false_alarm_rate) * 100:.1f}%"
        )

    else:

        st.metric(
            "False Alarm Rate",
            "N/A"
        )


# --------------------------------------------------
# Temperature graph
# --------------------------------------------------

st.subheader("Battery Temperature")

temperature_data = anomaly_df.pivot(
    index="Time (s)",
    columns="Cell",
    values="Temperature (°C)"
)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=temperature_data.index,
        y=temperature_data[1],
        mode="lines",
        name="Cell 1",
        line=dict(color="blue")
    )
)

fig.add_trace(
    go.Scatter(
        x=temperature_data.index,
        y=temperature_data[2],
        mode="lines",
        name="Cell 2",
        line=dict(color="pink")
    )
)

fig.add_trace(
    go.Scatter(
        x=temperature_data.index,
        y=temperature_data[3],
        mode="lines",
        name="Cell 3",
        line=dict(color="green")
    )
)

fig.add_trace(
    go.Scatter(
        x=temperature_data.index,
        y=temperature_data[4],
        mode="lines",
        name="Cell 4",
        line=dict(color="red")
    )
)

fig.update_layout(
    xaxis_title="Time (s)",
    yaxis_title="Temperature (°C)",
    legend_title="Cell"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Cell anomaly summary
# --------------------------------------------------

st.subheader("Cell Anomaly Summary")

cell_summary = (
    post_fault[
        post_fault["Status"] == "Anomaly"
    ]
    .groupby("Cell")
    .size()
    .reset_index(name="Anomaly Count")
)

cell_summary = cell_summary.sort_values(
    "Cell"
)

st.dataframe(
    cell_summary,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# SECTION 2
# NASA STATE-OF-HEALTH
# ==================================================

st.header("2. NASA B0006 Battery State-of-Health Estimation")

st.write(
    "NASA B0006 experimental battery-aging data "
    "is used independently for battery SoH estimation."
)


# --------------------------------------------------
# NASA main metrics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Predicted SoH",
        f"{latest_soh:.2f}%"
    )


with col2:

    st.metric(
        "Health Status",
        soh_status
    )


with col3:

    st.metric(
        "NASA Test Cycle",
        latest_cycle
    )


# --------------------------------------------------
# NASA model performance
# --------------------------------------------------

st.subheader("Linear Regression Performance")

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "MAE",
        f"{soh_mae:.2f}%"
    )


with col2:

    st.metric(
        "RMSE",
        f"{soh_rmse:.2f}%"
    )


# --------------------------------------------------
# NASA SoH graph
# --------------------------------------------------

st.subheader("Actual vs Predicted SoH")

soh_chart = soh_df.set_index("Cycle")[
    [
        "SoH (%)",
        "Predicted SoH (%)"
    ]
]

st.line_chart(
    soh_chart,
    use_container_width=True,
    color=["#1f77b4", "#ff7f0e"]
)


# ==================================================
# SECTION 3
# PROJECT SUMMARY
# ==================================================

st.header("3. BMS Summary")

st.info(
    "The thermal anomaly and NASA SoH results "
    "come from two complementary data sources. "
    "The simulation is used for cell-level thermal "
    "anomaly detection, while NASA B0006 data is "
    "used for battery health estimation."
)


# --------------------------------------------------
# Thermal summary
# --------------------------------------------------

st.write("### Thermal Monitoring")

if detected_cell is not None:

    st.write(
        f"**Status:** Thermal anomaly detected"
    )

    st.write(
        f"**Detected Cell:** Cell {detected_cell}"
    )

    st.write(
        f"**Detection Delay:** "
        f"{detection_delay} seconds"
    )

else:

    st.write(
        "**Status:** No thermal anomaly detected"
    )


# --------------------------------------------------
# SoH summary
# --------------------------------------------------

st.write("### Battery Health")

st.write(
    f"**NASA B0006 Predicted SoH:** "
    f"{latest_soh:.2f}%"
)

st.write(
    f"**Health Status:** {soh_status}"
)