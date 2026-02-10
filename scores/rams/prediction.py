"""
RAMS Score prediction engine.
"""

import math
from scores.rams.config import RISK_LEVELS


def compute_prediction(inputs: dict) -> dict:
    """
    Compute the RAMS score (1-10 scale) from raw input values.

    Args:
        inputs: dict mapping variable name to its raw value.

    Returns:
        dict with keys:
            - score: final RAMS score (1-10)
            - raw_value: pre-rounding value
            - risk_label: risk level string
            - risk_color: color for display
            - survival_24h: 24-hour survival percentage
            - components: list of per-component contribution dicts
    """
    age = float(inputs.get("age", 50))
    total_time = float(inputs.get("total_time_to_hospital_min", 15))
    auto_transport = int(inputs.get("auto_transport", 0))
    sbp = float(inputs.get("sbp", 120))
    hr = float(inputs.get("hr", 75))
    gcs = float(inputs.get("gcs", 15))
    height_in = float(inputs.get("height_in", 68))
    weight_lb = float(inputs.get("weight_lb", 170))
    bmi = (weight_lb / (height_in ** 2)) * 703
    rr = float(inputs.get("rr", 16))
    o2_sat = float(inputs.get("o2_sat", 98))
    fall = int(inputs.get("fall", 0))
    temp_f = float(inputs.get("temp_f", 98.6))

    components = [
        {
            "label": "A: Age \u2265 65",
            "condition": "Age \u2265 65",
            "met": age >= 65,
            "raw_points": 382,
        },
        {
            "label": "B: Transport Time 20-30 min",
            "condition": "20 \u2264 Time \u2264 30",
            "met": 20 <= total_time <= 30,
            "raw_points": 67,
        },
        {
            "label": "C: Auto Transport",
            "condition": "Auto = Yes",
            "met": auto_transport == 1,
            "raw_points": -57,
        },
        {
            "label": "D: SBP < 90 or HR < 60",
            "condition": "SBP < 90 or HR < 60",
            "met": sbp < 90 or hr < 60,
            "raw_points": 76,
        },
        {
            "label": "E: GCS \u2264 8 (Severe)",
            "condition": "GCS \u2264 8",
            "met": gcs <= 8,
            "raw_points": 1315,
        },
        {
            "label": "F: GCS 9-12 (Moderate)",
            "condition": "9 \u2264 GCS \u2264 12",
            "met": gcs > 8 and gcs < 13,
            "raw_points": 248,
        },
        {
            "label": "G: Underweight (BMI < 18.5)",
            "condition": "BMI < 18.5",
            "met": bmi < 18.5,
            "raw_points": 71,
        },
        {
            "label": "H: Class III Obesity (BMI \u2265 40)",
            "condition": "BMI \u2265 40",
            "met": bmi >= 40,
            "raw_points": 248,
        },
        {
            "label": "I: Resp Rate < 12",
            "condition": "RR < 12",
            "met": rr < 12,
            "raw_points": 73,
        },
        {
            "label": "J: Resp Rate > 20",
            "condition": "RR > 20",
            "met": rr > 20,
            "raw_points": 55,
        },
        {
            "label": "K: Hypoxic (O\u2082 Sat \u2264 92%)",
            "condition": "O\u2082 Sat \u2264 92%",
            "met": o2_sat <= 92,
            "raw_points": 95,
        },
        {
            "label": "L: Mechanism of Injury: Fall",
            "condition": "Fall = Yes",
            "met": fall == 1,
            "raw_points": 79,
        },
        {
            "label": "M: SBP \u2265 130 or HR > 80",
            "condition": "SBP \u2265 130 or HR > 80",
            "met": sbp >= 130 or hr > 80,
            "raw_points": -45,
        },
        {
            "label": "N: High Grade Temp (> 102.2\u00b0F)",
            "condition": "Temp > 102.2\u00b0F",
            "met": temp_f > 102.2,
            "raw_points": 61,
        },
    ]

    for comp in components:
        comp["value"] = comp["raw_points"] if comp["met"] else 0
        comp["log_contribution"] = math.log(1 + (comp["value"] / 100))

    raw_value = sum(c["log_contribution"] for c in components) + 2
    score = max(1, min(10, round(raw_value)))

    # Determine risk level and 24-hour survival
    risk_label = ""
    risk_color = "green"
    survival_24h = 0.0
    for level in RISK_LEVELS:
        if score <= level["max_score"]:
            risk_label = level["label"]
            risk_color = level["color"]
            survival_24h = level["survival_24h"]
            break

    return {
        "score": score,
        "raw_value": round(raw_value, 4),
        "risk_label": risk_label,
        "risk_color": risk_color,
        "survival_24h": survival_24h,
        "components": components,
    }
