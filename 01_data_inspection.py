"""
01_data_inspection.py
Inspect the reconstructed raw-like CSV. This dataset is synthetic reconstruction,
not the original workbook used in the tutorial.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "raw" / "churn_raw_reconstructed.csv")
print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum().sort_values(ascending=False))
print("\nExact duplicate rows:", df.duplicated().sum())
print("Duplicate Customer_ID rows:", df["Customer_ID"].duplicated().sum())
print("\nNumeric summary:\n", df.select_dtypes(include="number").describe().T)
