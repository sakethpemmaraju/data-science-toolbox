# 🧰 The Data Science Toolbox — Playbook

Seventeen notebooks + two scripts covering the day-to-day work of a data scientist or
data analyst: from raw extract to validated data, features, models, explanations,
monitoring, and management-ready reporting.

**Every notebook follows the same contract:**
1. It runs end-to-end on built-in **sample data** the moment you open it (`Kernel ▸ Restart & Run All`).
2. You plug in your own data by editing **one INPUT cell** (CSV / Excel / database).
3. You point it at your columns in **one CONFIG cell** (target, IDs, thresholds).
4. Everything it produces — charts, tables, models, scored files — lands in **`outputs/`**.

---

## 1. Task finder — "I need to…"

| I need to… | Open | Get out of it |
|---|---|---|
| …understand a dataset I've never seen | **01** EDA | profile, distributions, correlations, data-quality flags |
| …clean a messy extract | **05** Cleaning | `cleaned_data.csv` + an auditable `cleaning_log.csv` |
| …check a data refresh didn't break | **06** Validation | PASS/FAIL report against your data contract |
| …create and screen predictive features | **07** Feature engineering + WOE/IV | engineered dataset, IV ranking, WOE plots |
| …predict a yes/no outcome (default, churn, fraud) | **08** Leaderboard first, then **02/03/04** | champion model + deep-dive on the winner |
| …explain a model to stakeholders/regulators | **11** SHAP · **03** tree rules · **02** odds ratios | global drivers + per-record reason codes |
| …predict an amount or rate | **09** Regression | model bench + residual diagnostics |
| …find customer/portfolio segments | **10** Clustering | labeled data + nameable segment profiles |
| …turn probabilities into a credit-style score | **12** Calibration & scorecard | calibrated model, points scale, cutoff table |
| …check if my model/data has drifted | **13** Monitoring (PSI) | drift report with stable/watch/action flags |
| …analyze an A/B test or two-group comparison | **14** Stats & A/B | significance verdict, lift ± CI, sample-size calc |
| …forecast a monthly metric | **15** Time series (Part A) | 12-month forecast beating a naive baseline |
| …compare loan cohorts over time | **15** Vintage analysis (Part B) | vintage triangle, curves, deterioration flags |
| …send management a formatted summary | **16** Excel report | multi-sheet `portfolio_report.xlsx` with charts |
| …score new data on a schedule, no notebook | **`score_batch.py`** | scored CSV from any saved model |
| …check my environment is ready | **00** Start here | package check + folder index |

---

## 2. The standard plays

### 🆕 Play 1 — New dataset → production-grade model
```
06 Validation  →  05 Cleaning  →  01 EDA  →  07 Feature engineering
       →  08 Leaderboard (pick champion)  →  04/02/03 (deep-dive + tune the winner)
       →  11 SHAP (explain it)  →  12 Calibration & scorecard (make it usable)
```
Chain them through files: 05 writes `outputs/cleaned_data.csv`, 07 writes
`outputs/engineered_features.csv` — point the next notebook's `CSV_PATH` at them.

### 🔁 Play 2 — Monthly model health check
```
06 Validation (new month's data)  →  13 Monitoring (baseline vs current PSI)
       →  if PSI > 0.25 anywhere: retrain via Play 1  →  16 Excel report for the committee
```

### 🧪 Play 3 — Experiment / campaign readout
```
14 Stats & A/B — sample-size calculator BEFORE launch, significance + lift AFTER
```

### 📈 Play 4 — Portfolio review
```
15 Vintage analysis (cohort deterioration)  +  15 Forecasting (volume outlook)
       →  16 Excel report (package it for management)
```

### 👥 Play 5 — Segmentation study
```
01 EDA  →  10 Clustering (segment)  →  overlay outcomes by segment  →  16 report
```

---

## 3. How to execute any notebook

1. **Start Jupyter in this folder** (paths are relative):
   ```bash
   cd ml-modeling-notebooks
   jupyter lab          # or open the folder in VS Code
   ```
2. **First run: change nothing.** `Kernel ▸ Restart & Run All` on sample data to see
   the full output shape.
3. **Plug in your data** — the INPUT cell, one of:

   | Source | What to set |
   |---|---|
   | CSV | `DATA_SOURCE = "csv"`, `CSV_PATH = "data/yourfile.csv"` (drop the file in `data/`) |
   | Excel | `DATA_SOURCE = "excel"`, `EXCEL_PATH`, `EXCEL_SHEET` |
   | Database | `DATA_SOURCE = "database"`, `DB_CONNECTION_STRING`, `DB_QUERY` |

   Database connection strings (install the driver first — comments in the cell):
   ```
   sqlite:///data/my_database.db
   postgresql+psycopg2://user:password@host:5432/dbname      (pip install psycopg2-binary)
   mysql+pymysql://user:password@host:3306/dbname            (pip install pymysql)
   mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+18+for+SQL+Server   (pip install pyodbc)
   ```
4. **Edit the CONFIG cell** — target column, ID/leakage columns to drop, thresholds.
   Every editable cell is marked `EDIT THIS CELL`; everything else runs as-is.
5. **Restart & Run All again.** Collect results from `outputs/`.

### Command-line scoring (no notebook)
```bash
python score_batch.py --model outputs/xgboost.joblib \
    --input data/new_applications.csv --output outputs/scored.csv --threshold 0.30

# straight from a database:
python score_batch.py --model outputs/best_model.joblib \
    --db "postgresql+psycopg2://user:pass@host/db" \
    --query "SELECT * FROM applications WHERE score IS NULL" \
    --output outputs/scored.csv
```
Works with any `.joblib` the notebooks save — they are full pipelines, so raw feature
columns in = scores out. `utils.py` exposes the same loaders/metrics (`load_data`,
`psi`, `ks_stat`) for your own scripts.

---

## 4. Notebook reference

| # | Notebook | Needs a target? | Key outputs in `outputs/` |
|---|---|---|---|
| 00 | Start here | — | environment check |
| 01 | EDA | optional | `eda_profile.csv`, `eda_numeric_summary.csv`, charts |
| 02 | Logistic regression | binary | `logistic_regression.joblib`, `…_predictions.csv`, `…_coefficients.csv` |
| 03 | Decision tree | binary | `decision_tree.joblib`, `…_rules.txt`, diagram |
| 04 | XGBoost | binary | `xgboost.joblib`, `…_predictions.csv`, tuning cell |
| 05 | Cleaning & prep | no | `cleaned_data.csv`, `cleaning_log.csv` |
| 06 | Validation | no | `validation_report.csv` (set `FAIL_HARD=True` in pipelines) |
| 07 | Feature eng + WOE/IV | binary for IV | `engineered_features.csv`, `iv_summary.csv`, `woe_tables.csv` |
| 08 | Model leaderboard | binary | `model_leaderboard.csv`, `best_model.joblib`, ROC overlay |
| 09 | Regression | continuous | `regression_leaderboard.csv`, `regression_model.joblib` |
| 10 | Clustering | no | `segmented_data.csv`, `cluster_profile.csv` |
| 11 | SHAP explainability | binary | `reason_codes.csv`, beeswarm/waterfall charts |
| 12 | Calibration & scorecard | binary | `calibrated_model.joblib`, `scored_with_points.csv`, `score_band_table.csv` |
| 13 | Drift monitoring | optional | `monitoring_report.csv`, drift charts |
| 14 | Stats & A/B testing | group + outcome cols | `ab_test_results.csv`, sample-size answer |
| 15 | Time series & vintage | date + value / cohort data | `forecast_12m.csv`, `vintage_triangle.csv` |
| 16 | Excel reporting | scored file | `portfolio_report.xlsx` |

---

## 5. Field guide — thresholds and gotchas

**Metric cheat sheet**

| Metric | Where | Rule of thumb |
|---|---|---|
| AUC / Gini (=2·AUC−1) | 02/03/04/08 | 0.5 = random; credit models typically land AUC 0.65–0.80 |
| KS | 08 | max separation of good/bad score distributions; 0.25+ respectable |
| IV | 07 | <0.02 useless · 0.02–0.1 weak · 0.1–0.3 medium · 0.3–0.5 strong · >0.5 **check for leakage** |
| PSI | 13 | <0.10 stable · 0.10–0.25 investigate · >0.25 act |
| Brier | 12 | lower = better-calibrated probabilities |
| MAPE | 15 | only trust a forecast that beats the seasonal-naive baseline |

**Gotchas the notebooks guard against — but you should know:**
- **Leakage**: any feature only knowable *after* the outcome inflates every metric.
  Suspiciously high AUC or IV > 0.5 → audit `DROP_COLS` first.
- **Class imbalance**: rare-event models (default, fraud) use `class_weight="balanced"` /
  `scale_pos_weight` here. That distorts raw probabilities — recalibrate (12) before
  using them as probabilities rather than rankings.
- **The 0.50 cutoff is arbitrary**: pick thresholds from the trade-off tables
  (02 §7b, 12 band table), matched to the cost of each error type.
- **Peeking at A/B tests**: checking significance repeatedly mid-test inflates false
  positives. Size the test first (14 §6), read out once.
- **Train/test discipline**: all evaluation here is on held-out data; keep it that way
  when you modify the notebooks.

---

## 6. Setup

```bash
pip install -r requirements.txt
```
Note the pin `xgboost==2.0.3` — newer wheels need a newer OpenMP runtime than
Anaconda ships on macOS. `catboost` is optional (extra bench model in 08, strongest
on high-cardinality categoricals); notebook 08 picks up whichever boosters are
installed and skips the rest gracefully.

```
ml-modeling-notebooks/
├── data/              <- your input files go here
├── outputs/           <- everything produced lands here
├── 00–16 *.ipynb      <- the notebooks
├── score_batch.py     <- CLI batch scorer
├── utils.py           <- shared loaders + metrics for your own scripts
├── requirements.txt
└── PLAYBOOK.md        <- this file
```
