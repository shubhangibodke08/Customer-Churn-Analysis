"""
02_data_cleaning.py
Reproducible cleaning pipeline for the reconstructed raw-like dataset.
Important: raw file is a labelled reconstruction from the uploaded processed CSV,
with intentionally introduced quality issues. It is not the tutorial's original raw workbook.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "churn_raw_reconstructed.csv"
OUTPUT = ROOT / "data" / "processed" / "churn_cleaned.csv"

df = pd.read_csv(INPUT)
print("Before cleaning:", df.shape)

# 1. Trim whitespace in text columns.
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace({"": pd.NA, "Unknown": pd.NA, "unknown": pd.NA})

# 2. Standardize categories.
df["Customer_Name"] = df["Customer_Name"].str.title()
df["Gender"] = df["Gender"].str.title()
df["City"] = df["City"].str.title()
df["State"] = df["State"].str.title().replace({"Up": "Uttar Pradesh"})
df["Subscription_Type"] = df["Subscription_Type"].str.title()
df["Payment_Method"] = df["Payment_Method"].str.title().replace({"Upi": "UPI"})
df["Internet_Service"] = df["Internet_Service"].str.upper()
df["Tech_Support"] = df["Tech_Support"].str.title()
df["Senior_Citizen"] = df["Senior_Citizen"].str.title()
df["Dependents"] = df["Dependents"].str.title()
df["Churn"] = df["Churn"].str.title()
df["Contract_Type"] = df["Contract_Type"].replace({"Month-To-Month": "Month-to-Month"})

# 3. Convert numeric columns and apply basic validity rules.
numeric_cols = ["Age", "Tenure_Months", "Monthly_Charges", "Total_Charges"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.loc[~df["Age"].between(18, 100), "Age"] = np.nan
df.loc[~df["Tenure_Months"].between(0, 72), "Tenure_Months"] = np.nan
df.loc[df["Monthly_Charges"] < 0, "Monthly_Charges"] = np.nan
df.loc[df["Total_Charges"] < 0, "Total_Charges"] = np.nan

# 4. Parse mixed date formats; invalid dates become NaT.
df["Last_Interaction_Date"] = pd.to_datetime(
    df["Last_Interaction_Date"], format="mixed", dayfirst=True, errors="coerce"
)

# 5. Deduplicate.
before = len(df)
df = df.drop_duplicates()
print("Exact duplicates removed:", before - len(df))

before = len(df)
df = df.drop_duplicates(subset=["Customer_ID"], keep="first")
print("Repeated Customer_ID rows removed:", before - len(df))

# 6. Recompute derived fields; don't trust stale derived columns.
df["Monthly_Revenue"] = df["Monthly_Charges"]
df["Tenure_Group"] = pd.cut(
    df["Tenure_Months"],
    bins=[-0.001, 12, 36, 48, 72],
    labels=["0-12 months", "13-36 months", "37-48 months", "49-72 months"],
    include_lowest=True
).astype("string")
df["Senior"] = np.where(df["Age"].ge(60), "Senior Citizen", "Adult")
df.loc[df["Age"].isna(), "Senior"] = "Unknown"
df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0}).astype("Int64")

df = df.sort_values("Customer_ID").reset_index(drop=True)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")

print("After cleaning:", df.shape)
print("Remaining duplicate IDs:", df["Customer_ID"].duplicated().sum())
print("Saved:", OUTPUT)
