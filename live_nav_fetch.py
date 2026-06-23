import requests
import pandas as pd
import os

def fetch_single_nav(scheme_code=125497):
    """
    Fetches the live NAV history for a specific mutual fund scheme from mfapi.in,
    parses the JSON response, and saves it as a CSV file in data/raw/.
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching live NAV data from: {url}")
    
    try:
        # 1. Make the GET request
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        # 2. Parse the JSON response
        json_data = response.json()
        
        # mfapi.in returns a 'status' field we can check
        if json_data.get("status") != "SUCCESS":
            print(f"Failed to retrieve data for scheme {scheme_code}.")
            return
            
        # Extract metadata and NAV history
        meta = json_data.get("meta", {})
        nav_data = json_data.get("data", [])
        
        scheme_name = meta.get('scheme_name', 'Unknown Scheme')
        print(f"Successfully fetched data for: {scheme_name}")
        print(f"Total NAV records retrieved: {len(nav_data)}")
        
        # 3. Convert to Pandas DataFrame
        df = pd.DataFrame(nav_data)
        
        # Add the scheme_code as a column so we can join it with our master data later
        df['scheme_code'] = scheme_code
        
        # Reorder columns for neatness
        df = df[['scheme_code', 'date', 'nav']]
        
        # 4. Save as raw CSV
        output_dir = "data/raw"
        os.makedirs(output_dir, exist_ok=True)  # Failsafe: ensures folder exists
        
        output_filename = f"live_nav_{scheme_code}.csv"
        output_path = os.path.join(output_dir, output_filename)
        
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ Data saved successfully to: {output_path}")
        print("\n--- First 5 Rows ---")
        print(df.head())
        
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # 125497 is the AMFI code for HDFC Top 100
    fetch_single_nav(scheme_code=125497)