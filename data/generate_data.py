import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_dataset(output_path="data/synthetic_fb_data.csv"):
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(" Generating synthetic data...")
    
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    dates.reverse()
    data = []
    
    # Generate "Ad Fatigue" Scenario
    for i, date in enumerate(dates):
        freq = 1.2 + (i * 0.08) 
        ctr = max(0.005, 0.025 - (i * 0.0006))
        
        spend = 1000
        imps = int((spend / 20) * 1000) 
        clicks = int(imps * ctr)
        revenue = clicks * 2.5 * 60 
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "campaign_name": "Prospecting_USA",  
            "adset_name": "Broad_Targeting",     
            "spend": spend,
            "impressions": imps,
            "clicks": clicks,
            "frequency": round(freq, 2),
            "revenue": round(revenue, 2)
        })
            
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f" Success! Data saved to: {output_path}")

if __name__ == "__main__":
    generate_dataset()