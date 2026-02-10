"""
Clinical Scoring Tools - Landing Page
"""

import streamlit as st
import importlib
import os

st.set_page_config(page_title="Clinical Scoring Tools", layout="wide")

st.title("Clinical Scoring Tools")
st.markdown(
    "A collection of validated bedside clinical scoring tools for trauma patients. "
    "Select a score from the sidebar or click below to get started."
)

st.divider()

# Auto-discover scores by scanning scores/ for subdirectories with config.py
scores_dir = os.path.join(os.path.dirname(__file__), "scores")
discovered = []

for entry in sorted(os.listdir(scores_dir)):
    entry_path = os.path.join(scores_dir, entry)
    if os.path.isdir(entry_path) and os.path.exists(
        os.path.join(entry_path, "config.py")
    ):
        try:
            mod = importlib.import_module(f"scores.{entry}.config")
            meta = getattr(mod, "SCORE_META", None)
            if meta:
                discovered.append({"key": entry, "meta": meta})
        except Exception:
            pass

# Display score cards
cols = st.columns(len(discovered)) if discovered else []
for i, score_info in enumerate(discovered):
    meta = score_info["meta"]
    with cols[i]:
        st.subheader(meta["name"])
        st.caption(meta["tagline"])
        st.markdown(f"**Score range:** {meta['score_range']}")
        st.markdown(f"**Outcome:** {meta['outcome_label']}")
        # Find the matching page file
        key = score_info["key"]
        page_files = {
            "ford": "pages/1_FORD_Score.py",
            "rams": "pages/2_RAMS_Score.py",
        }
        if key in page_files:
            st.page_link(page_files[key], label=f"Open {meta['name']}", icon="🏥")

st.divider()
st.caption("For research and educational purposes only. Not a substitute for clinical judgment.")
