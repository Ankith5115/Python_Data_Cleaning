import pandas as pd
import numpy as np

# ── 1. Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv(r"A:\Python_data_cleaning\Job_market_dataset.csv")

print("=== RAW DATA OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ── 2. Missing values ─────────────────────────────────────────────────────────
print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "No missing values found.")

# Drop rows where critical columns are null
critical_cols = ["Job_Title", "Salary_USD", "Job_Growth_Projection"]
before = len(df)
df.dropna(subset=critical_cols, inplace=True)
print(f"Dropped {before - len(df)} rows with nulls in critical columns.")

# Fill non-critical nulls with sensible defaults
df["Remote_Friendly"] = df["Remote_Friendly"].fillna("Unknown")
df["Required_Skills"] = df["Required_Skills"].fillna("Not Specified")

# ── 3. Duplicates ─────────────────────────────────────────────────────────────
print("\n=== DUPLICATES ===")
dupes = df.duplicated().sum()
print(f"Duplicate rows found: {dupes}")
df.drop_duplicates(inplace=True)

# ── 4. Standardise string columns ────────────────────────────────────────────
print("\n=== STANDARDISING STRINGS ===")
str_cols = ["Job_Title", "Industry", "Company_Size", "Location",
            "AI_Adoption_Level", "Automation_Risk", "Required_Skills",
            "Remote_Friendly", "Job_Growth_Projection"]

for col in str_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# Normalise Yes/No variants
df["Remote_Friendly"] = df["Remote_Friendly"].replace(
    {"Yes": "Yes", "No": "No", "True": "Yes", "False": "No", "1": "Yes", "0": "No"}
)

print("String columns stripped and title-cased.")

# ── 5. Validate categoricals ──────────────────────────────────────────────────
print("\n=== CATEGORICAL VALIDATION ===")

expected = {
    "Company_Size":          {"Small", "Medium", "Large"},
    "AI_Adoption_Level":     {"Low", "Medium", "High"},
    "Automation_Risk":       {"Low", "Medium", "High"},
    "Remote_Friendly":       {"Yes", "No", "Unknown"},
    "Job_Growth_Projection": {"Growth", "Stable", "Decline"},
}

for col, valid_values in expected.items():
    bad = ~df[col].isin(valid_values)
    if bad.any():
        print(f"  {col}: {bad.sum()} unexpected value(s) → {df.loc[bad, col].unique()}")
        df = df[~bad]
    else:
        print(f"  {col}: OK")

# ── 6. Numeric cleaning ───────────────────────────────────────────────────────
print("\n=== NUMERIC CLEANING (Salary_USD) ===")
df["Salary_USD"] = pd.to_numeric(df["Salary_USD"], errors="coerce")

# Drop rows where salary couldn't be parsed
salary_nulls = df["Salary_USD"].isnull().sum()
if salary_nulls:
    print(f"Dropping {salary_nulls} rows with unparseable Salary_USD.")
    df.dropna(subset=["Salary_USD"], inplace=True)

# Round to 2 decimal places
df["Salary_USD"] = df["Salary_USD"].round(2)

# Flag outliers using IQR
Q1 = df["Salary_USD"].quantile(0.25)
Q3 = df["Salary_USD"].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
outliers = df[(df["Salary_USD"] < lower) | (df["Salary_USD"] > upper)]
print(f"Salary range after cleaning: ${df['Salary_USD'].min():,.2f} – ${df['Salary_USD'].max():,.2f}")
print(f"IQR outliers flagged (not dropped): {len(outliers)}")
df["Salary_Outlier"] = df["Salary_USD"].apply(lambda x: x < lower or x > upper)

# ── 7. Encode categoricals ────────────────────────────────────────────────────
ordinal_map = {"Low": 1, "Medium": 2, "High": 3}
df["AI_Adoption_Level_Enc"] = df["AI_Adoption_Level"].map(ordinal_map)
df["Automation_Risk_Enc"]   = df["Automation_Risk"].map(ordinal_map)
df["Remote_Friendly_Enc"]   = df["Remote_Friendly"].map({"No": 0, "Yes": 1, "Unknown": -1})

# ── 8. Summary stats ──────────────────────────────────────────────────────────
print("\n=== CLEANED DATA SUMMARY ===")
print(f"Final shape: {df.shape}")
print(f"\nSalary stats:\n{df['Salary_USD'].describe().round(2)}")
print(f"\nJob growth distribution:\n{df['Job_Growth_Projection'].value_counts()}")
print(f"\nRemote-friendly distribution:\n{df['Remote_Friendly'].value_counts()}")

# ── 9. Save cleaned data ──────────────────────────────────────────────────────
output_path = r"A:\Python_data_cleaning\Job_market_dataset_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"\nCleaned dataset saved to: {output_path}")
