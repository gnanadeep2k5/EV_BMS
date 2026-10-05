def make_decision(anomaly_detected, cell_id, soh):

    if anomaly_detected and soh < 80:
        return {
            "Risk Level": "HIGH",
            "Status": "HIGH RISK",
            "Affected Cell": cell_id,
            "Recommendation": "SERVICE RECOMMENDED"
        }

    elif anomaly_detected and soh >= 80:
        return {
            "Risk Level": "MEDIUM",
            "Status": "THERMAL WARNING",
            "Affected Cell": cell_id,
            "Recommendation": "MONITOR AFFECTED CELL"
        }

    elif not anomaly_detected and soh < 80:
        return {
            "Risk Level": "MEDIUM",
            "Status": "BATTERY HEALTH WARNING",
            "Affected Cell": "None",
            "Recommendation": "BATTERY INSPECTION RECOMMENDED"
        }

    else:
        return {
            "Risk Level": "LOW",
            "Status": "NORMAL",
            "Affected Cell": "None",
            "Recommendation": "CONTINUE MONITORING"
        }


if __name__ == "__main__":

    print("\nDecision Engine Test")
    print("--------------------")

    print("\nTest 1: Normal")
    print(make_decision(False, None, 95))

    print("\nTest 2: Thermal anomaly")
    print(make_decision(True, 3, 95))

    print("\nTest 3: Low SoH")
    print(make_decision(False, None, 70))

    print("\nTest 4: Thermal anomaly + Low SoH")
    print(make_decision(True, 3, 70))