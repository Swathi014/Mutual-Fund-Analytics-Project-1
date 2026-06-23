import requests
import pandas as pd
import os
import time

def fetch_multiple_navs():
    """
    Loops through 5 specific bluechip mutual fund schemes, fetches their live 
    NAV history from mfapi.in, and saves each as an independent raw CSV file.
    """
    # Dictionary mapping Scheme Names to their unique AMFI scheme codes
    schemes = {
        "SBI_Bluechip": 119551,
        "ICICI_Bluechip": 120503,
        "Nippon_Large_Cap": 118632,
        "Axis_Bluechip": 119092,
        "Kotak_Bluechip": 120841
    }
    
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)  # Ensure data/raw folder exists
    
    print(f"Starting batch fetch for {len(schemes)} schemes...\n")
    print("=" * 50)
    
    for name, code in schemes.items():
        url = f"https://api.mfapi.in/mf/{code}"
        print(f"🔄 Fetching {name} (Code: {code})...")
        
        try:
            # 1. Send GET request
            response = requests.get(url)
            response.raise_for_status()
            
            # 2. Parse JSON response
            json_data = response.json()
            
            if json_data.get("status") != "SUCCESS":
                print(f"❌ Failed to get successful status for {name}")
                continue
                
            meta = json_data.get("meta", {})
            nav_data = json_data.get("data", [])
            
            # 3. Process data into DataFrame
            df = pd.DataFrame(nav_data)
            
            if df.empty:
                print(f"⚠️ No historical records returned for {name}")
                continue
                
            # Add scheme_code metadata column
            df['scheme_code'] = code
            df = df[['scheme_code', 'date', 'nav']]
            
            # 4. Save to separate CSV
            output_filename = f"raw_nav_{code}.csv"
            output_path = os.path.join(output_dir, output_filename)
            df.to_csv(output_path, index=False)
            
            print(f"✅ Saved {len(df)} rows to {output_path}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error for {name}: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error for {name}: {e}")
            
        # Polite API practice: brief sleep to prevent rate limits
        print("-" * 50)
        time.sleep(1) 
        
    print("\n All downloads completed successfully!")

if __name__ == "__main__":
    fetch_multiple_navs()