# src/process_financials.py
"""
Read raw CSV (data/raw/finance_operations.csv), compute AbsoluteProfitCHF and ProfitMargin,
save to data/processed/finance_operations_processed.csv.
Works regardless of current working directory.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "finance_operations.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = PROCESSED_DIR / "finance_operations_processed.csv"

if not RAW_PATH.exists():
    raise SystemExit(f"Raw CSV not found at {RAW_PATH}. Run src/create_synthetic_data.py first or place your raw CSV there.")

df = pd.read_csv(RAW_PATH)
# try to be flexible about column names
rev_col = next((c for c in df.columns if c.lower().startswith("revenue")), None)
cost_col = next((c for c in df.columns if c.lower().startswith("cost")), None)

if rev_col is None or cost_col is None:
    raise SystemExit(f"Could not find revenue/cost columns in {RAW_PATH}. Columns found: {df.columns.tolist()}")

# ensure numeric
df[rev_col] = pd.to_numeric(df[rev_col], errors="coerce").fillna(0.0)
df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce").fillna(0.0)

# compute absolute profit and profit margin (safe division)
df["AbsoluteProfitCHF"] = df[rev_col] - df[cost_col]
df["ProfitMargin"] = df.apply(
    lambda r: (r["AbsoluteProfitCHF"] / r[rev_col]) if r[rev_col] != 0 else np.nan,
    axis=1
)
df["ProfitMargin"] = df["ProfitMargin"].round(4)

# save processed CSV
df.to_csv(OUT_PATH, index=False)
print(f"Wrote processed data to: {OUT_PATH}  (rows: {len(df)})")

