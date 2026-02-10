"""
PRIME-ICU Score prediction engine.
"""

import math
from scores.prime_icu.config import RISK_LEVELS


def compute_prediction(inputs: dict) -> dict:
    """
    Compute the PRIME-ICU score (1-10 scale) from raw input values.

    Args:
        inputs: dict mapping variable name to its raw value.

    Returns:
        dict with keys:
            - score: final PRIME-ICU score (1-10)
            - raw_value: pre-rounding value
            - risk_label: risk level string
            - risk_color: color for display
            - icu_admission_pct: ICU admission percentage
            - components: list of per-component contribution dicts
    """
    age = float(inputs.get("age", 50))
    sex = inputs.get("sex", "Male")
    bmi = float(inputs.get("bmi", 25.0))
    gcs = float(inputs.get("gcs", 15))
    sbp = float(inputs.get("sbp", 120))
    hr = float(inputs.get("hr", 75))
    rr = float(inputs.get("rr", 16))
    o2_sat = float(inputs.get("o2_sat", 98))
    temp_f = float(inputs.get("temp_f", 98.6))
    transport_mode = inputs.get("transport_mode", "Other")
    transferred = int(inputs.get("transferred", 0))
    departure_to_hospital = float(inputs.get("departure_to_hospital_min", 15))
    time_on_scene = float(inputs.get("time_on_scene_min", 15))
    total_time = float(inputs.get("total_time_min", 15))
    mechanism = inputs.get("mechanism", "Other")
    industrial = int(inputs.get("industrial", 0))

    components = [
        # Age
        {
            "label": "Age 45-64",
            "condition": "45 \u2264 Age \u2264 64",
            "met": 45 <= age <= 64,
            "raw_points": 28,
        },
        {
            "label": "Age \u2265 65",
            "condition": "Age \u2265 65",
            "met": age >= 65,
            "raw_points": 72,
        },
        # Sex
        {
            "label": "Male",
            "condition": "Sex = Male",
            "met": sex == "Male",
            "raw_points": 24,
        },
        # GCS
        {
            "label": "GCS Severe (\u2264 8)",
            "condition": "GCS \u2264 8",
            "met": gcs <= 8,
            "raw_points": 805,
        },
        {
            "label": "GCS Moderate (9-12)",
            "condition": "9 \u2264 GCS \u2264 12",
            "met": 9 <= gcs <= 12,
            "raw_points": 347,
        },
        # BMI
        {
            "label": "Class III Obesity (BMI \u2265 40)",
            "condition": "BMI \u2265 40",
            "met": bmi >= 40,
            "raw_points": -84,
        },
        # SBP
        {
            "label": "Hypotensive (SBP < 90)",
            "condition": "SBP < 90",
            "met": sbp < 90,
            "raw_points": 80,
        },
        {
            "label": "Elevated BP (SBP 120-129)",
            "condition": "120 \u2264 SBP \u2264 129",
            "met": 120 <= sbp <= 129,
            "raw_points": -34,
        },
        {
            "label": "Stage 1 HTN (SBP 130-139)",
            "condition": "130 \u2264 SBP \u2264 139",
            "met": 130 <= sbp <= 139,
            "raw_points": -37,
        },
        {
            "label": "Stage 2 HTN (SBP \u2265 140)",
            "condition": "SBP \u2265 140",
            "met": sbp >= 140,
            "raw_points": -39,
        },
        # Heart Rate
        {
            "label": "Tachycardic (HR \u2265 100)",
            "condition": "HR \u2265 100",
            "met": hr >= 100,
            "raw_points": 38,
        },
        # Respiratory Rate
        {
            "label": "Low RR (< 12)",
            "condition": "RR < 12",
            "met": rr < 12,
            "raw_points": -49,
        },
        {
            "label": "High RR (> 20)",
            "condition": "RR > 20",
            "met": rr > 20,
            "raw_points": 93,
        },
        # O2 Sat
        {
            "label": "Hypoxic (O\u2082 Sat \u2264 92%)",
            "condition": "O\u2082 Sat \u2264 92%",
            "met": o2_sat <= 92,
            "raw_points": 70,
        },
        # Temperature
        {
            "label": "Hypothermia (< 95\u00b0F)",
            "condition": "Temp < 95\u00b0F",
            "met": temp_f < 95,
            "raw_points": 104,
        },
        {
            "label": "Low Grade Fever (99.1-100.4\u00b0F)",
            "condition": "99.1 \u2264 Temp \u2264 100.4\u00b0F",
            "met": 99.1 <= temp_f <= 100.4,
            "raw_points": -19,
        },
        {
            "label": "High Grade Fever (> 102.2\u00b0F)",
            "condition": "Temp > 102.2\u00b0F",
            "met": temp_f > 102.2,
            "raw_points": 40,
        },
        # Transport Mode
        {
            "label": "Ambulance Transport",
            "condition": "Transport = Ambulance",
            "met": transport_mode == "Ambulance",
            "raw_points": 208,
        },
        {
            "label": "Auto/Cab Transport",
            "condition": "Transport = Auto/Cab",
            "met": transport_mode == "Auto/Cab",
            "raw_points": -27,
        },
        {
            "label": "Police Transport",
            "condition": "Transport = Police",
            "met": transport_mode == "Police",
            "raw_points": -39,
        },
        {
            "label": "Air Helicopter Transport",
            "condition": "Transport = Air Helicopter",
            "met": transport_mode == "Air Helicopter",
            "raw_points": 154,
        },
        {
            "label": "Walked In",
            "condition": "Transport = Walked",
            "met": transport_mode == "Walked",
            "raw_points": -47,
        },
        # Transfer
        {
            "label": "Transferred",
            "condition": "Transferred = Yes",
            "met": transferred == 1,
            "raw_points": 81,
        },
        # Industrial
        {
            "label": "Industrial Accident",
            "condition": "Industrial = Yes",
            "met": industrial == 1,
            "raw_points": -17,
        },
        # Mechanism
        {
            "label": "Penetrating Mechanism",
            "condition": "Mechanism = Penetrating",
            "met": mechanism == "Penetrating",
            "raw_points": 33,
        },
        {
            "label": "Blunt Mechanism",
            "condition": "Mechanism = Blunt",
            "met": mechanism == "Blunt",
            "raw_points": 65,
        },
        {
            "label": "Mechanism Not Available",
            "condition": "Mechanism = Not Available",
            "met": mechanism == "Not Available",
            "raw_points": 49,
        },
        # Departure to Hospital
        {
            "label": "Departure-to-Hospital \u2264 10 min",
            "condition": "DTH \u2264 10 min",
            "met": departure_to_hospital <= 10,
            "raw_points": 27,
        },
        # Time on Scene
        {
            "label": "Time on Scene 20-30 min",
            "condition": "20 \u2264 TOS \u2264 30",
            "met": 20 <= time_on_scene <= 30,
            "raw_points": -25,
        },
        # Total Time
        {
            "label": "Total Time 20-30 min",
            "condition": "20 \u2264 TOT \u2264 30",
            "met": 20 <= total_time <= 30,
            "raw_points": 24,
        },
        {
            "label": "Total Time > 80 min",
            "condition": "TOT > 80 min",
            "met": total_time > 80,
            "raw_points": -30,
        },
    ]

    for comp in components:
        comp["value"] = comp["raw_points"] if comp["met"] else 0
        comp["log_contribution"] = math.log(1 + (comp["value"] / 100))

    raw_value = sum(c["log_contribution"] for c in components) + 3
    score = max(1, min(10, round(raw_value)))

    # Determine risk level and ICU admission percentage
    risk_label = ""
    risk_color = "green"
    icu_admission_pct = 0.0
    for level in RISK_LEVELS:
        if score <= level["max_score"]:
            risk_label = level["label"]
            risk_color = level["color"]
            icu_admission_pct = level["icu_admission_pct"]
            break

    return {
        "score": score,
        "raw_value": round(raw_value, 4),
        "risk_label": risk_label,
        "risk_color": risk_color,
        "icu_admission_pct": icu_admission_pct,
        "components": components,
    }
