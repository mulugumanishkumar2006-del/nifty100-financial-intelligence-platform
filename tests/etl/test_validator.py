import pandas as pd

from src.etl.dq_rules import (
    dq01_primary_key_uniqueness,
    dq05_positive_sales,
)


def test_dq01_pass():

    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    passed, _ = dq01_primary_key_uniqueness(df, "id")

    assert passed


def test_dq01_fail():

    df = pd.DataFrame({
        "id": [1, 1, 2]
    })

    passed, _ = dq01_primary_key_uniqueness(df, "id")

    assert not passed


def test_positive_sales():

    df = pd.DataFrame({
        "sales": [100, 200, 300]
    })

    passed, _ = dq05_positive_sales(df)

    assert passed