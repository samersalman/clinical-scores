"""
PRIME-ICU Score - Variable definitions for the input form.
"""

MODEL_NAME = "PRIME-ICU Score"

RISK_LEVELS = [
    {"max_score": 3, "label": "Low Risk", "color": "green", "icu_admission_pct": 5.7},
    {"max_score": 5, "label": "Moderate Risk", "color": "orange", "icu_admission_pct": 25.8},
    {"max_score": 6, "label": "High Risk", "color": "red", "icu_admission_pct": 59.5},
    {"max_score": 10, "label": "Highest Risk", "color": "red", "icu_admission_pct": 81.4},
]

VARIABLES = [
    # --- Demographics ---
    {
        "name": "age",
        "label": "Age (years)",
        "type": "continuous",
        "min": 0,
        "max": 120,
        "step": 1,
        "default": 50,
        "group": "Demographics",
    },
    {
        "name": "sex",
        "label": "Sex",
        "type": "categorical",
        "options": ["Male", "Female"],
        "group": "Demographics",
    },
    {
        "name": "bmi",
        "label": "BMI (kg/m\u00b2)",
        "type": "continuous",
        "min": 10.0,
        "max": 80.0,
        "step": 0.1,
        "default": 25.0,
        "group": "Demographics",
    },
    # --- Vitals ---
    {
        "name": "gcs",
        "label": "Glasgow Coma Scale (3-15)",
        "type": "continuous",
        "min": 3,
        "max": 15,
        "step": 1,
        "default": 15,
        "group": "Vitals",
    },
    {
        "name": "sbp",
        "label": "Systolic Blood Pressure (mmHg)",
        "type": "continuous",
        "min": 40,
        "max": 260,
        "step": 1,
        "default": 120,
        "group": "Vitals",
    },
    {
        "name": "hr",
        "label": "Heart Rate (bpm)",
        "type": "continuous",
        "min": 20,
        "max": 220,
        "step": 1,
        "default": 75,
        "group": "Vitals",
    },
    {
        "name": "rr",
        "label": "Respiratory Rate (breaths/min)",
        "type": "continuous",
        "min": 4,
        "max": 50,
        "step": 1,
        "default": 16,
        "group": "Vitals",
    },
    {
        "name": "o2_sat",
        "label": "Oxygen Saturation (%)",
        "type": "continuous",
        "min": 50.0,
        "max": 100.0,
        "step": 1.0,
        "default": 98.0,
        "group": "Vitals",
    },
    {
        "name": "temp_f",
        "label": "Temperature (\u00b0F)",
        "type": "continuous",
        "min": 90.0,
        "max": 110.0,
        "step": 0.1,
        "default": 98.6,
        "group": "Vitals",
    },
    # --- Transport ---
    {
        "name": "transport_mode",
        "label": "Transport Mode",
        "type": "categorical",
        "options": ["Ambulance", "Auto/Cab", "Police", "Air Helicopter", "Walked", "Other"],
        "group": "Transport",
    },
    {
        "name": "transferred",
        "label": "Transferred from Another Facility",
        "type": "categorical",
        "options": {"No": 0, "Yes": 1},
        "group": "Transport",
    },
    {
        "name": "departure_to_hospital_min",
        "label": "Departure-to-Hospital (minutes)",
        "type": "continuous",
        "min": 0,
        "max": 120,
        "step": 1,
        "default": 15,
        "group": "Transport",
    },
    {
        "name": "time_on_scene_min",
        "label": "Time on Scene (minutes)",
        "type": "continuous",
        "min": 0,
        "max": 120,
        "step": 1,
        "default": 15,
        "group": "Transport",
    },
    {
        "name": "total_time_min",
        "label": "Total Time Notify-to-Hospital (minutes)",
        "type": "continuous",
        "min": 0,
        "max": 300,
        "step": 1,
        "default": 15,
        "group": "Transport",
    },
    # --- Mechanism ---
    {
        "name": "mechanism",
        "label": "Mechanism of Injury",
        "type": "categorical",
        "options": ["Penetrating", "Blunt", "Not Available", "Other"],
        "group": "Mechanism",
    },
    {
        "name": "industrial",
        "label": "Industrial Accident",
        "type": "categorical",
        "options": {"No": 0, "Yes": 1},
        "group": "Mechanism",
    },
]

SCORE_META = {
    "name": "PRIME-ICU Score",
    "tagline": "Presentation Risk Index for Monitoring and Escalation to ICU",
    "description": (
        "The **Presentation Risk Index for Monitoring and Escalation to ICU (PRIME-ICU)** "
        "is a bedside predictive tool for ICU admission in trauma patients.\n\n"
        "It produces a score from **1\u201310** using patient demographics, vital signs, "
        "transport details, and mechanism of injury. Higher scores indicate greater risk "
        "of ICU admission.\n\n"
        "**How to use:** Fill in the fields below, click **Calculate**, and review the "
        "score, risk level, and component breakdown."
    ),
    "score_range": "1\u201310",
    "outcome_key": "icu_admission_pct",
    "outcome_label": "ICU Admission Risk",
    "risk_table_score_label": "PRIME-ICU Score",
    "risk_table_outcome_key": "icu_admission_pct",
    "risk_table_outcome_label": "ICU Admission",
    "component_points_key": "raw_points",
    "component_points_label": "Raw Points",
    "component_extra_key": "log_contribution",
    "component_extra_label": "log(1 + x/100)",
    "chart_key": "log_contribution",
    "chart_label": "log Contribution",
    "highlight_color": "#2d4a3e",
    "highlight_text_color": "#ffffff",
}
