"""
Shared UI renderer for all clinical scoring tools.
"""

import streamlit as st
import pandas as pd
from collections import OrderedDict


def render_score_page(config_module, prediction_module):
    """Render a complete score page from config metadata and prediction engine."""
    meta = config_module.SCORE_META
    variables = config_module.VARIABLES
    risk_levels = config_module.RISK_LEVELS

    st.set_page_config(page_title=meta["name"], layout="wide")
    st.title(meta["name"])

    with st.expander(f"About the {meta['name']}", expanded=False):
        st.markdown(meta["description"])

    # --- Build grouped variable structure ---
    groups = OrderedDict()
    for var in variables:
        group = var.get("group", "General")
        groups.setdefault(group, []).append(var)

    # --- Input Form ---
    inputs = {}

    with st.form("prediction_form"):
        for group_name, group_vars in groups.items():
            with st.expander(group_name, expanded=True):
                cols = st.columns(2)
                for i, var in enumerate(group_vars):
                    col = cols[i % 2]
                    with col:
                        if var["type"] == "continuous":
                            inputs[var["name"]] = st.number_input(
                                var["label"],
                                min_value=float(var["min"]),
                                max_value=float(var["max"]),
                                value=float(var["default"]),
                                step=float(var["step"]),
                                key=var["name"],
                            )
                        elif var["type"] == "categorical":
                            if isinstance(var["options"], dict):
                                # RAMS-style: display keys, pass mapped values
                                options = list(var["options"].keys())
                                selected = st.selectbox(
                                    var["label"],
                                    options=options,
                                    key=var["name"],
                                )
                                inputs[var["name"]] = var["options"][selected]
                            else:
                                # FORD-style: pass string directly
                                selected = st.selectbox(
                                    var["label"],
                                    options=var["options"],
                                    key=var["name"],
                                )
                                inputs[var["name"]] = selected

        submitted = st.form_submit_button(
            "Calculate", type="primary", use_container_width=True
        )

    # --- Results ---
    if submitted:
        result = prediction_module.compute_prediction(inputs)
        score = result["score"]

        st.divider()
        st.subheader("Result")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label=f"{meta['name']} ({meta['score_range']})",
                value=f"{score}",
            )
        with col2:
            st.markdown(
                f"### :{result['risk_color']}[{result['risk_label']}]"
            )
        with col3:
            outcome_val = result[meta["outcome_key"]]
            st.metric(label=meta["outcome_label"], value=f"{outcome_val}%")

        # --- Risk level reference table ---
        st.subheader("Risk Level Reference")
        ref_rows = []
        prev_max = -1
        for level in risk_levels:
            low = prev_max + 1
            high = level["max_score"]
            if low == high:
                score_range = str(low)
            else:
                score_range = f"{low}\u2013{high}"
            ref_rows.append(
                {
                    meta["risk_table_score_label"]: score_range,
                    "Risk Level": level["label"],
                    meta["risk_table_outcome_label"]: f"{level[meta['risk_table_outcome_key']]}%",
                }
            )
            prev_max = high
        ref_df = pd.DataFrame(ref_rows)

        hl_color = meta["highlight_color"]
        hl_text = meta["highlight_text_color"]

        def highlight_current(row):
            if row["Risk Level"] == result["risk_label"]:
                return [
                    f"background-color: {hl_color}; color: {hl_text}"
                ] * len(row)
            return [""] * len(row)

        st.dataframe(
            ref_df.style.apply(highlight_current, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        # --- Component Breakdown ---
        st.subheader("Component Breakdown")

        components = result["components"]
        rows = []
        for c in components:
            row = {
                "Predictor": c["label"],
                "Condition": c["condition"],
                "Met?": "Yes" if c["met"] else "No",
                meta["component_points_label"]: c[meta["component_points_key"]]
                if c["met"]
                else 0,
            }
            if meta["component_extra_key"]:
                row[meta["component_extra_label"]] = round(
                    c[meta["component_extra_key"]], 4
                )
            rows.append(row)

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- Bar chart of active components ---
        st.subheader("Active Components")
        active = [c for c in components if c["met"]]
        if active:
            chart_df = pd.DataFrame(
                {
                    "Component": [c["label"] for c in active],
                    meta["chart_label"]: [
                        round(c[meta["chart_key"]], 4)
                        if isinstance(c[meta["chart_key"]], float)
                        else c[meta["chart_key"]]
                        for c in active
                    ],
                }
            )
            chart_df = chart_df.sort_values(
                meta["chart_label"], key=abs, ascending=True
            )
            chart_df = chart_df.set_index("Component")
            st.bar_chart(chart_df, horizontal=True)
        else:
            st.info("No risk factors are present with the current inputs.")
