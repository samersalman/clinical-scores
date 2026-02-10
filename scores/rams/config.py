"""
RAMS Score - Variable definitions for the input form.
"""

MODEL_NAME = "RAMS Score"

RISK_LEVELS = [
    {"max_score": 4, "label": "Low Risk", "color": "green", "survival_24h": 99.88},
    {"max_score": 5, "label": "Moderate Risk", "color": "orange", "survival_24h": 97.69},
    {"max_score": 6, "label": "High Risk", "color": "red", "survival_24h": 89.92},
    {"max_score": 10, "label": "Highest Risk", "color": "red", "survival_24h": 65.71},
]

VARIABLES = [
    # --- Patient Demographics ---
    {
        "name": "age",
        "label": "Age (years)",
        "type": "continuous",
        "min": 0,
        "max": 120,
        "step": 1,
        "default": 50,
        "group": "Patient Demographics",
    },
    {
        "name": "bmi",
        "label": "Body Mass Index (BMI)",
        "type": "continuous",
        "min": 10.0,
        "max": 60.0,
        "step": 0.1,
        "default": 25.0,
        "group": "Patient Demographics",
    },
    {
        "name": "temp_f",
        "label": "Temperature (\u00b0F)",
        "type": "continuous",
        "min": 90.0,
        "max": 110.0,
        "step": 0.1,
        "default": 98.6,
        "group": "Patient Demographics",
    },
    # --- Vitals ---
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
    # --- Neurological ---
    {
        "name": "gcs",
        "label": "Glasgow Coma Scale (3-15)",
        "type": "continuous",
        "min": 3,
        "max": 15,
        "step": 1,
        "default": 15,
        "group": "Neurological",
    },
    # --- Transport ---
    {
        "name": "total_time_to_hospital_min",
        "label": "Total Time to Hospital (minutes)",
        "type": "continuous",
        "min": 0,
        "max": 180,
        "step": 1,
        "default": 15,
        "group": "Transport",
    },
    {
        "name": "auto_transport",
        "label": "Transport by Automobile",
        "type": "categorical",
        "options": {"No": 0, "Yes": 1},
        "group": "Transport",
    },
    # --- Mechanism of Injury ---
    {
        "name": "fall",
        "label": "Mechanism of Injury: Fall",
        "type": "categorical",
        "options": {"No": 0, "Yes": 1},
        "group": "Mechanism of Injury",
    },
]

SCORE_META = {
    "name": "RAMS Score",
    "tagline": "Rapid Acuity and Mortality Score",
    "description": (
        "The **Rapid Acuity and Mortality Score (RAMS)** is a bedside predictive tool "
        "for 24-hour mortality in trauma patients.\n\n"
        "It produces a score from **1\u201310** using patient demographics, vital signs, "
        "neurological status, transport details, and mechanism of injury. Higher scores "
        "indicate greater mortality risk.\n\n"
        "**How to use:** Fill in the fields below, click **Calculate**, and review the "
        "score, risk level, and component breakdown."
    ),
    "score_range": "1\u201310",
    "outcome_key": "survival_24h",
    "outcome_label": "24-Hour Survival",
    "risk_table_score_label": "RAMS Score",
    "risk_table_outcome_key": "survival_24h",
    "risk_table_outcome_label": "24-Hour Survival",
    "component_points_key": "raw_points",
    "component_points_label": "Raw Points",
    "component_extra_key": "log_contribution",
    "component_extra_label": "log(1 + x/100)",
    "chart_key": "log_contribution",
    "chart_label": "log Contribution",
    "highlight_color": "#2d4a3e",
    "highlight_text_color": "#ffffff",
}
