"""
Data Quality Rules
Sprint 1 - Day 3
"""

import pandas as pd


def dq01_primary_key_uniqueness(df: pd.DataFrame, key_column: str):
    """
    DQ-01: Check if primary key values are unique.
    """
    duplicates = df[df.duplicated(subset=[key_column], keep=False)]

    if duplicates.empty:
        return True, None

    return False, duplicates


def dq02_company_year_uniqueness(df: pd.DataFrame):
    """
    DQ-02: Check uniqueness of (company_id, year).
    """

    if "company_id" not in df.columns or "year" not in df.columns:
        return True, None

    duplicates = df[df.duplicated(subset=["company_id", "year"], keep=False)]

    if duplicates.empty:
        return True, None

    return False, duplicates


def dq03_foreign_key_integrity(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    foreign_key: str,
):
    """
    DQ-03: Check foreign key integrity.
    """

    invalid = child_df[
        ~child_df[foreign_key].isin(parent_df[foreign_key])
    ]

    if invalid.empty:
        return True, None

    return False, invalid

def dq04_balance_sheet(df: pd.DataFrame):
    """
    Assets ≈ Liabilities + Equity
    """

    required = ["total_assets", "total_liabilities", "equity"]

    if not all(col in df.columns for col in required):
        return True, None

    tolerance = 0.01

    invalid = df[
        abs(
            df["total_assets"] -
            (df["total_liabilities"] + df["equity"])
        ) > tolerance
    ]

    if invalid.empty:
        return True, None

    return False, invalid

def dq05_positive_sales(df: pd.DataFrame):
    """
    Sales should never be negative.
    """

    if "sales" not in df.columns:
        return True, None

    invalid = df[df["sales"] < 0]

    if invalid.empty:
        return True, None

    return False, invalid

import re

def dq06_valid_urls(df: pd.DataFrame):

    if "website" not in df.columns:
        return True, None

    pattern = re.compile(r"^https?://")

    invalid = df[
        ~df["website"].fillna("").str.match(pattern)
    ]

    if invalid.empty:
        return True, None

    return False, invalid

def dq07_net_cash(df):

    if "net_cash" not in df.columns:
        return True, None

    invalid = df[df["net_cash"] < 0]

    if invalid.empty:
        return True, None

    return False, invalid

def dq08_tax_rate(df):

    if "tax_percentage" not in df.columns:
        return True, None

    invalid = df[
        (df["tax_percentage"] < 0) |
        (df["tax_percentage"] > 100)
    ]

    if invalid.empty:
        return True, None

    return False, invalid

def dq09_dividend(df):

    if "dividend_payout" not in df.columns:
        return True, None

    invalid = df[df["dividend_payout"] > 100]

    if invalid.empty:
        return True, None

    return False, invalid

def dq10_eps(df):

    if "eps" not in df.columns:
        return True, None

    invalid = df[df["eps"].isnull()]

    if invalid.empty:
        return True, None

    return False, invalid

def dq11_company_name(df):

    if "company_name" not in df.columns:
        return True, None

    invalid = df[df["company_name"].isnull()]

    if invalid.empty:
        return True, None

    return False, invalid

def dq12_duplicate_company(df):

    if "company_name" not in df.columns:
        return True, None

    duplicates = df[
        df.duplicated(
            subset=["company_name"],
            keep=False
        )
    ]

    if duplicates.empty:
        return True, None

    return False, duplicates

def dq13_missing_year(df):

    if "year" not in df.columns:
        return True, None

    invalid = df[df["year"].isnull()]

    if invalid.empty:
        return True, None

    return False, invalid

def dq14_mandatory(df):

    mandatory = ["company_id"]

    if not all(col in df.columns for col in mandatory):
        return True, None

    invalid = df[df["company_id"].isnull()]

    if invalid.empty:
        return True, None

    return False, invalid

import re

def dq15_ticker(df):

    if "company_id" not in df.columns:
        return True, None

    pattern = re.compile(r"^[A-Z0-9]+$")

    invalid = df[
        ~df["company_id"].astype(str).str.match(pattern)
    ]

    if invalid.empty:
        return True, None

    return False, invalid

def dq16_dataset_coverage(df):

    if len(df) < 90:
        return False, df

    return True, None


if __name__ == "__main__":

    companies = pd.DataFrame({
        "company_id": ["ABB", "ABB", "TCS"]
    })

    result, data = dq01_primary_key_uniqueness(
        companies,
        "company_id"
    )

    print(result)

    if data is not None:
        print(data)