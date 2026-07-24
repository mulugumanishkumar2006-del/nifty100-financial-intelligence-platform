"""
Utility Functions for API

NIFTY100 Financial Intelligence Platform
"""

import json
import math
import pandas as pd
import numpy as np
from typing import Any


# ==========================================================
# Custom JSON Encoder
# ==========================================================

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NumPy scalars, NaN and Infinity values"""
    
    def default(self, o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            value = float(o)
            if math.isnan(value) or math.isinf(value):
                return None
            return value
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return None
        return super().default(o)


# ==========================================================
# Clean Data
# ==========================================================

def clean_value(value: Any) -> Any:
    """Recursively clean values by replacing NaN and Infinity with None"""
    if isinstance(value, dict):
        return {k: clean_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [clean_value(v) for v in value]
    elif isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    elif isinstance(value, np.generic):
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            value = float(value)
            if math.isnan(value) or math.isinf(value):
                return None
            return value
        if isinstance(value, np.bool_):
            return bool(value)
    return value


# ==========================================================
# Clean Dataframe
# ==========================================================

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataframe by replacing NaN and Infinity values with None
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    if df is None or df.empty:
        return df
    
    # Replace NaN with None
    df = df.where(pd.notna(df), None)
    
    # Replace Infinity with None
    for col in df.columns:
        if df[col].dtype in ['float64', 'float32']:
            df[col] = df[col].apply(lambda x: None if isinstance(x, float) and math.isinf(x) else x)
    
    return df


# ==========================================================
# Convert DataFrame to Records
# ==========================================================

def dataframe_to_records(df: pd.DataFrame) -> list:
    """
    Convert DataFrame to list of dictionaries with NaN/Infinity handling
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        List of dictionaries
    """
    if df is None or df.empty:
        return []
    
    df = clean_dataframe(df)
    records = df.to_dict(orient="records")
    return [clean_value(record) for record in records]
