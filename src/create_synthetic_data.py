# create_synthetic_data.py
"""
Génère des données synthétiques internes pour le projet banque/finance
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Dossier pour sauvegarder les CSV
RAW = Path("../data/raw") #.. means "go one folder up relative to the CWD, not relative to the script file

RAW.mkdir(parents=True, exist_ok=True)

# Paramètres synthétiques
months = pd.date_range("2024-01-01", periods=12, freq="MS")
products = ["Equity", "Bonds", "ETF"]
client_segments = ["Private", "Corporate", "Institutional"]

rows = []
for m in months:
    for p in products:
        for s in client_segments:
            revenue = int(np.random.randint(100_000, 500_000))
            cost = int(revenue * np.random.uniform(0.35, 0.65))
            rows.append({
                "Month": m,
                "Product": p,
                "ClientSegment": s,
                "RevenueCHF": revenue,
                "CostCHF": cost
            })

df = pd.DataFrame(rows)
df.to_csv(RAW / "finance_operations.csv", index=False)

print("Données synthétiques créées dans :", RAW.resolve())

