# Clinical Scoring Tools

Unified multi-page Streamlit app hosting validated clinical scoring tools.

## Running the App

- Install: `pip install -r requirements.txt`
- Run: `streamlit run Home.py`

## Architecture

```
Home.py                    Landing page (auto-discovers scores)
pages/N_<Name>_Score.py    3-line stubs calling shared UI
scores/<name>/config.py    Variable definitions, risk levels, SCORE_META
scores/<name>/prediction.py  Scoring engine (compute_prediction)
shared/ui.py               Shared render_score_page() function
```

Data flow: page stub imports config + prediction modules, passes them to `render_score_page()` which reads `SCORE_META` to render the form, results, risk table, component breakdown, and bar chart.

## Adding a New Score

1. Create `scores/<name>/config.py` with `VARIABLES`, `RISK_LEVELS`, `SCORE_META`
2. Create `scores/<name>/prediction.py` with `compute_prediction(inputs) -> dict`
3. Create `pages/N_<Name>_Score.py` (3-line stub)
4. Push to GitHub — auto-redeploys on Streamlit Community Cloud

## Key Rules

- **Never modify prediction logic** — these are validated clinical tools
- All UI variation is driven by `SCORE_META` dict in each score's config
- Landing page auto-discovers scores from `scores/` directory
