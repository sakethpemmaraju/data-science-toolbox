# 🧰 Data Science Toolbox

[![notebooks](https://github.com/sakethpemmaraju/data-science-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/sakethpemmaraju/data-science-toolbox/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Seventeen self-contained Jupyter notebooks + CLI scripts covering the day-to-day work
of a data scientist / data analyst: EDA, cleaning, validation, feature engineering
(WOE/IV), classification & regression modeling, clustering, explainability (SHAP),
calibration & scorecards, drift monitoring, A/B testing, time-series & vintage
analysis, and automated Excel reporting.

**➡️ Start with [PLAYBOOK.md](PLAYBOOK.md)** — the "which notebook for which task"
guide, standard workflows, and execution instructions.
**➡️ Or open `00_start_here.ipynb`** for the in-Jupyter index + environment check.

## Quick start

```bash
pip install -r requirements.txt
cd ml-modeling-notebooks
jupyter lab
```

Open any notebook and **Run All** — every one works immediately on built-in synthetic
lending data. To use your own data, edit the single cell marked
`INPUT — EDIT THIS CELL` (CSV / Excel / SQL database) and the `CONFIG` cell
(target column, columns to drop), then Run All again. Every result lands in `outputs/`.

For a real analysis, stamp a dedicated workspace so this template stays clean:

```bash
python new_project.py ~/work/my-analysis
```

## Contents

| Stage | Notebooks |
|---|---|
| Data in shape | 05 Cleaning · 06 Validation · 01 EDA |
| Features | 07 Feature engineering + WOE/IV |
| Modeling | 08 Leaderboard · 02 Logistic · 03 Tree · 04 XGBoost · 09 Regression · 10 Clustering |
| Trust | 11 SHAP explainability · 12 Calibration & scorecard |
| Operate | 13 Drift monitoring (PSI) · `score_batch.py` |
| Analyze & report | 14 Stats/A-B testing · 15 Time series & vintage · 16 Excel report |

All notebooks have been executed end-to-end; the saved copies include live results
so you can preview each one's output before running it. CI re-executes every
notebook on each push, so the badge above proves the toolbox runs.

Note: `data/` and `outputs/` are gitignored — anything you put there (including
real datasets) stays on your machine and is never committed.

MIT licensed — see [LICENSE](LICENSE).
