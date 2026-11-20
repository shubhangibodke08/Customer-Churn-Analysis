"""
03_exploratory_analysis.py
Creates summary tables and charts from the cleaned customer dataset.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "churn_cleaned.csv")

df["Churn_Flag"] = pd.to_numeric(df["Churn_Flag"], errors="coerce")
n = df["Customer_ID"].nunique()
churned = int(df["Churn_Flag"].sum())
print(f"Customers: {n}")
print(f"Churned: {churned}")
print(f"Churn rate: {churned/n:.1%}")
print(f"Average monthly charge: {df['Monthly_Charges'].mean():.2f}")

for col in ["Contract_Type", "Subscription_Type", "Tech_Support", "State"]:
    result = df.groupby(col, dropna=False).agg(
        Customers=("Customer_ID", "nunique"),
        Churned=("Churn_Flag", "sum")
    )
    result["Churn_Rate"] = result["Churned"] / result["Customers"]
    print(f"\nChurn by {col}:\n", result.sort_values("Churn_Rate", ascending=False))

OUT = ROOT / "reports" / "generated_charts"
OUT.mkdir(parents=True, exist_ok=True)

for col, filename, title in [
    ("Contract_Type", "churn_by_contract.png", "Churn rate by contract type"),
    ("Subscription_Type", "churn_by_plan.png", "Churn rate by subscription plan"),
    ("Tech_Support", "churn_by_support.png", "Churn rate by technical support"),
]:
    temp = df.groupby(col).agg(
        Customers=("Customer_ID", "nunique"),
        Churned=("Churn_Flag", "sum")
    )
    temp["Churn_Rate"] = temp["Churned"] / temp["Customers"]
    ax = (temp["Churn_Rate"] * 100).sort_values().plot(kind="bar", figsize=(8, 4))
    ax.set_title(title)
    ax.set_ylabel("Churn rate (%)")
    ax.set_xlabel("")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()
