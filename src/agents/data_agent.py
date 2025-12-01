import pandas as pd
import json
import numpy as np
from .base import BaseAgent
from src.schema import validate_schema, check_data_drift

class DataAgent(BaseAgent):
    def __init__(self, path="data/synthetic_fb_data.csv"):
        super().__init__("DataAgent")
        self.path = path

    def execute(self, query):
        # 1. Load & Validate (Governance)
        try:
            df = pd.read_csv(self.path)
            validate_schema(df) 
        except Exception as e:
            return {"error": f"Data Governance Failure: {str(e)}"}

        # 2. Check Statistical Drift (Adaptivity)
        drift_warnings = check_data_drift(df)

        # 3. Calculate "Baseline vs Current" Deltas (The V2 Requirement)
        # We split data into "Last 7 Days" (Current) vs "Previous 23 Days" (Baseline)
        df['date'] = pd.to_datetime(df['date'])
        max_date = df['date'].max()
        cutoff_date = max_date - pd.Timedelta(days=7)
        
        current = df[df['date'] > cutoff_date]
        baseline = df[df['date'] <= cutoff_date]
        
        metrics = {}
        # Calculate % Change for key metrics
        for metric in ['spend', 'revenue', 'clicks', 'impressions']:
            curr_avg = current[metric].mean()
            base_avg = baseline[metric].mean()
            
            # Avoid divide by zero
            if base_avg > 0:
                delta = ((curr_avg - base_avg) / base_avg) * 100
            else:
                delta = 0
            
            metrics[metric] = {
                "current_avg": round(curr_avg, 2),
                "baseline_avg": round(base_avg, 2),
                "delta_percent": round(delta, 2)
            }

        # Calculate ROAS manually for accuracy
        curr_roas = current['revenue'].sum() / current['spend'].sum() if current['spend'].sum() > 0 else 0
        base_roas = baseline['revenue'].sum() / baseline['spend'].sum() if baseline['spend'].sum() > 0 else 0
        roas_delta = ((curr_roas - base_roas) / base_roas) * 100 if base_roas > 0 else 0

        metrics['roas'] = {
            "current": round(curr_roas, 2),
            "baseline": round(base_roas, 2),
            "delta_percent": round(roas_delta, 2)
        }

        # Return a structured analysis object
        return {
            "analysis_period": "Last 7 Days vs Previous 30 Days",
            "metrics": metrics,
            "drift_warnings": drift_warnings,
            "data_health_check": "Passed"
        }