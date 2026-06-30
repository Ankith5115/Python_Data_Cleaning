# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python data cleaning and analysis project using a job market dataset (`Job_market_dataset.csv`). The CSV contains 10 columns covering job titles, industries, salaries, automation risk, and job growth projections across global locations.

## Files

| File | Purpose |
|---|---|
| `dataset.py` | Original script — loads CSV and prints `df.head()` |
| `python_code.py` | Full data cleaning pipeline (see below) |
| `Job_market_dataset.csv` | Raw input data |
| `Job_market_dataset_cleaned.csv` | Output of `python_code.py` (generated) |

## Running the Scripts

```powershell
# Original loader
python dataset.py

# Full data cleaning pipeline
python python_code.py
```

Dependencies: `pandas`, `numpy` — install via `pip install pandas numpy`.

## Data Cleaning Pipeline (`python_code.py`)

The pipeline runs these steps in order:

1. **Load** — reads the raw CSV, prints shape and dtypes
2. **Missing values** — drops rows with nulls in `Job_Title`, `Salary_USD`, `Job_Growth_Projection`; fills `Remote_Friendly` → `"Unknown"` and `Required_Skills` → `"Not Specified"`
3. **Duplicates** — removes exact duplicate rows
4. **String standardisation** — strips whitespace and title-cases all text columns; normalises Yes/No variants
5. **Categorical validation** — validates `Company_Size`, `AI_Adoption_Level`, `Automation_Risk`, `Remote_Friendly`, `Job_Growth_Projection` against expected value sets; drops rows with unexpected values
6. **Numeric cleaning** — coerces `Salary_USD` to float, rounds to 2 dp, flags IQR outliers in a new `Salary_Outlier` boolean column
7. **Encoding** — adds ordinal integer encodings: `AI_Adoption_Level_Enc`, `Automation_Risk_Enc` (`Low=1, Medium=2, High=3`), `Remote_Friendly_Enc` (`No=0, Yes=1, Unknown=-1`)
8. **Save** — writes cleaned data to `Job_market_dataset_cleaned.csv`

## Dataset Schema

`Job_market_dataset.csv` columns:
- `Job_Title`, `Industry`, `Company_Size`, `Location`
- `AI_Adoption_Level`, `Automation_Risk` — categorical (`Low`/`Medium`/`High`)
- `Required_Skills` — single skill string
- `Salary_USD` — float
- `Remote_Friendly` — `Yes`/`No`
- `Job_Growth_Projection` — `Growth`/`Stable`/`Decline`

## Notes

- All file paths in both scripts are hardcoded to `A:\Python_data_cleaning\` — update if the project moves.
- `Job_market_dataset_cleaned.csv` is a generated file; do not edit it manually.
