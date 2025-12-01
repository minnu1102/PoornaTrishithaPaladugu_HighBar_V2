import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional

# --- 1. Explicit Schema Definition (Pydantic) ---
class AdPerformanceRecord(BaseModel):
    date: str
    campaign_name: str
    adset_name: str
    spend: float = Field(ge=0, description="Daily spend must be non-negative")
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    frequency: float = Field(ge=1.0, description="Frequency cannot be less than 1")
    revenue: float = Field(ge=0)

# --- 2. Schema Validation Layer ---
def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates every row against the Pydantic schema.
    Returns cleaned DataFrame or raises error with specific row details.
    """
    errors = []
    # Convert dataframe to dictionary records for validation
    records = df.to_dict(orient='records')
    
    for i, record in enumerate(records):
        try:
            # Pydantic validation happens here
            AdPerformanceRecord(**record)
        except ValidationError as e:
            errors.append(f"Row {i} Error: {e}")
            
    if errors:
        # If any errors found, stop the pipeline immediately (Governance)
        error_msg = "\n".join(errors[:5]) # Show first 5 errors to avoid flooding logs
        raise ValueError(f"Schema Validation Failed:\n{error_msg}")
    
    return df

# --- 3. Adaptive Drift Detection (Statistical Check) ---
def check_data_drift(df: pd.DataFrame, threshold_std: float = 3.0) -> Dict[str, str]:
    """
    Checks if current data distribution deviates significantly from the mean.
    Uses Z-Score to detect anomalies (Adaptivity).
    """
    drift_report = {}
    numeric_cols = ['spend', 'frequency', 'revenue', 'ctr']
    
    # Calculate CTR manually since it might not be in schema
    if 'ctr' not in df.columns and 'impressions' in df.columns:
        df['ctr'] = df['clicks'] / df['impressions'].replace(0, 1)

    for col in numeric_cols:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            max_val = df[col].max()
            
            # If max value is > 3 standard deviations from mean, flag it
            if std > 0:
                z_score = (max_val - mean) / std
                if z_score > threshold_std:
                    drift_report[col] = f"High Drift Detected (Z-Score: {z_score:.2f})"
    
    return drift_report