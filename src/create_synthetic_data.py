# src/create_synthetic_data.py
"""
Generate synthetic internal operational data for analysis projects.
This robust version ensures the CSV is always saved inside the project folder
regardless of where the script is run from.
"""

from pathlib import Path    # For handling file and folder paths safely
import pandas as pd         # For creating and handling tabular data
import numpy as np          # For generating random numbers

# ------------------- 1. Determine project root -------------------
# __file__ -> path of this script: = "create_synthetic_data.py" (relative path) or "src/create_synthetic_data.py" depending on how you run it.
# Path() converts a string path into a Path object
# .resolve() -> absolute canonical path
# .parent -> folder containing this script ('src')
# .parent.parent -> project root folder

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ------------------- 2. Define raw data folder -------------------
RAW = PROJECT_ROOT / "data" / "raw" 
RAW.mkdir(parents=True, exist_ok=True)  # create folder if missing

# ------------------- 3. Parameters for synthetic data -------------------
months = pd.date_range("2024-01-01", periods=12, freq="MS")  # first day of each month
products = ["Equity", "Bonds", "ETF"]
client_segments = ["Private", "Corporate", "Institutional"]

# ------------------- 4. Generate synthetic rows -------------------
rows = []
for m in months:
    for p in products:
        for s in client_segments:
            revenue = int(np.random.randint(100_000, 500_000))        # Random revenue
            cost = int(revenue * np.random.uniform(0.35, 0.65))       # Cost is 35%-65% of revenue
            rows.append({
                "Month": m,
                "Product": p,
                "ClientSegment": s,
                "RevenueCHF": revenue,
                "CostCHF": cost
            })

# ------------------- 5. Save to CSV -------------------
df = pd.DataFrame(rows)
out_path = RAW / "finance_operations.csv"
df.to_csv(out_path, index=False)  # index=False avoids adding a row index column

print("Données synthétiques créées dans :", out_path)
