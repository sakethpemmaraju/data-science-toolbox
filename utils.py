"""Shared helpers for the data-science toolbox.

Import from a notebook or script in this folder:

    from utils import load_data, make_sample_lending_data, psi, ks_stat
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_data(source: str = "csv", *, csv_path: str = "data/my_data.csv",
              excel_path: str = "data/my_data.xlsx", excel_sheet=0,
              db_connection_string: str = "sqlite:///data/my_database.db",
              db_query: str = "SELECT * FROM loans") -> pd.DataFrame:
    """One data loader for every input type used across the notebooks.

    source: "csv" | "excel" | "database" | "sample"
    """
    if source == "csv":
        return pd.read_csv(csv_path)
    if source == "excel":
        return pd.read_excel(excel_path, sheet_name=excel_sheet)
    if source == "database":
        from sqlalchemy import create_engine
        return pd.read_sql(db_query, create_engine(db_connection_string))
    if source == "sample":
        return make_sample_lending_data()
    raise ValueError(f"Unknown source: {source!r}")


def make_sample_lending_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Synthetic consumer-lending dataset with a binary default_flag target,
    a continuous interest_rate target, and realistic missingness."""
    rng = np.random.default_rng(seed)
    fico = rng.normal(690, 55, n).clip(500, 850).round()
    dti = rng.normal(28, 10, n).clip(1, 65).round(1)
    loan_amount = rng.lognormal(9.4, 0.5, n).clip(1000, 50000).round(-2)
    income = rng.lognormal(11.1, 0.45, n).clip(15000, 400000).round(-2)
    utilization = rng.beta(2, 3, n).round(3) * 100
    tenure_months = rng.integers(0, 240, n)
    grade = rng.choice(list("ABCDE"), n, p=[0.25, 0.30, 0.25, 0.13, 0.07])
    purpose = rng.choice(["debt_consolidation", "credit_card", "home_improvement",
                          "auto", "medical", "other"], n,
                         p=[0.38, 0.22, 0.13, 0.12, 0.06, 0.09])
    state = rng.choice(["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA"], n)
    grade_rate = pd.Series(grade).map({"A": 7.5, "B": 10.5, "C": 13.5,
                                       "D": 17.0, "E": 21.0}).values
    interest_rate = (grade_rate - 0.010 * (fico - 690) + 0.02 * (dti - 28)
                     + rng.normal(0, 0.8, n)).clip(5, 30).round(2)
    origination_date = (pd.Timestamp("2023-01-01")
                        + pd.to_timedelta(rng.integers(0, 36, n) * 30, unit="D")).normalize()
    logit = (-4.2 - 0.012 * (fico - 690) + 0.045 * (dti - 28)
             + 0.018 * (utilization - 40)
             + 0.35 * np.isin(grade, ["D", "E"]).astype(float)
             + 0.20 * (purpose == "debt_consolidation").astype(float))
    default_flag = rng.binomial(1, 1 / (1 + np.exp(-logit)))
    df = pd.DataFrame({
        "loan_id": np.arange(1, n + 1),
        "origination_date": origination_date,
        "fico_score": fico, "dti": dti, "loan_amount": loan_amount,
        "annual_income": income, "revolving_utilization": utilization,
        "employment_tenure_months": tenure_months, "grade": grade,
        "loan_purpose": purpose, "state": state,
        "interest_rate": interest_rate, "default_flag": default_flag,
    })
    for col, frac in [("dti", 0.03), ("annual_income", 0.05),
                      ("employment_tenure_months", 0.02)]:
        df.loc[df.sample(frac=frac, random_state=seed).index, col] = np.nan
    return df


def psi(baseline, current, bins: int = 10) -> float:
    """Population Stability Index between two samples of one variable.
    < 0.10 stable | 0.10-0.25 moderate shift | > 0.25 significant shift."""
    baseline, current = pd.Series(baseline).dropna(), pd.Series(current).dropna()
    if pd.api.types.is_numeric_dtype(baseline) and baseline.nunique() > bins:
        edges = np.unique(np.quantile(baseline, np.linspace(0, 1, bins + 1)))
        edges[0], edges[-1] = -np.inf, np.inf
        b = pd.cut(baseline, edges).value_counts(normalize=True, sort=False)
        c = pd.cut(current, edges).value_counts(normalize=True, sort=False)
    else:
        cats = sorted(set(baseline.unique()) | set(current.unique()), key=str)
        b = baseline.value_counts(normalize=True).reindex(cats).fillna(0)
        c = current.value_counts(normalize=True).reindex(cats).fillna(0)
    b, c = b.clip(lower=1e-4), c.clip(lower=1e-4)
    return float(((c - b) * np.log(c / b)).sum())


def ks_stat(y_true, proba) -> float:
    """Kolmogorov-Smirnov statistic: max separation between the score
    distributions of the two classes. Common credit-model metric."""
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(y_true, proba)
    return float(np.max(tpr - fpr))
