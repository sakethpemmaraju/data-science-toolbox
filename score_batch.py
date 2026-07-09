#!/usr/bin/env python3
"""Batch-score a file or database table with any model saved by the notebooks.

The saved .joblib files are full pipelines (imputation + encoding + model),
so the input just needs the same feature columns that were used in training.

Examples:
    python score_batch.py --model outputs/xgboost.joblib \
        --input data/new_applications.csv --output outputs/scored_batch.csv

    python score_batch.py --model outputs/best_model.joblib \
        --db "sqlite:///data/my_database.db" \
        --query "SELECT * FROM applications WHERE scored_at IS NULL" \
        --output outputs/scored_batch.csv --threshold 0.30
"""
import argparse
import sys

import joblib
import pandas as pd


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="path to a .joblib pipeline")
    ap.add_argument("--input", help="input CSV (or use --db/--query)")
    ap.add_argument("--db", help="SQLAlchemy connection string")
    ap.add_argument("--query", help="SQL query returning rows to score")
    ap.add_argument("--output", required=True, help="output CSV path")
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="probability cutoff for the prediction column (default 0.5)")
    args = ap.parse_args()

    if args.input:
        df = pd.read_csv(args.input)
    elif args.db and args.query:
        from sqlalchemy import create_engine
        df = pd.read_sql(args.query, create_engine(args.db))
    else:
        ap.error("provide --input CSV, or both --db and --query")

    model = joblib.load(args.model)
    print(f"Loaded {args.model}; scoring {len(df):,} rows...")

    if hasattr(model, "predict_proba"):          # classifier
        df["probability"] = model.predict_proba(df)[:, 1]
        df["prediction"] = (df["probability"] >= args.threshold).astype(int)
        print(f"Mean probability: {df['probability'].mean():.4f} | "
              f"flagged at >= {args.threshold}: {df['prediction'].mean():.2%}")
    else:                                        # regressor
        df["prediction"] = model.predict(df)
        print(f"Mean prediction: {df['prediction'].mean():.4f}")

    df.to_csv(args.output, index=False)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
