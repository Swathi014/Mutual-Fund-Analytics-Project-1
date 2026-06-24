import pandas as pd
import os

def clean_nav_data():
    input_path = 'data/raw/02_nav_history.csv'
    output_path = 'data/processed/clean_nav.csv'
    
    print("=" * 50)
    print("🧹 TASK 1: CLEANING NAV HISTORY")
    print("=" * 50)
    
    try:
        # 1. Load the dataset
        print(f"Loading {input_path}...")
        df = pd.read_csv(input_path)
        initial_rows = len(df)
        
        # 2. Parse dates to datetime
        print("Parsing dates to datetime...")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Drop rows where date parsing failed
        df = df.dropna(subset=['date'])
        
        # 3. Sort by amfi_code and date (Updated!)
        print("Sorting data...")
        df = df.sort_values(by=['amfi_code', 'date'])
        
        # 4. Remove duplicates (Updated!)
        print("Removing duplicates...")
        df = df.drop_duplicates(subset=['amfi_code', 'date'], keep='last')
        
        # 5. Forward-fill missing NAVs (to handle holidays/weekends)
        print("Forward-filling missing NAV values...")
        # Group by amfi_code to ensure we only ffill within the same fund (Updated!)
        df['nav'] = df.groupby('amfi_code')['nav'].ffill()
        
        # 6. Validate NAV > 0
        print("Validating NAV > 0...")
        df = df[df['nav'] > 0]
        
        # 7. Save to processed folder
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv(output_path, index=False)
        
        final_rows = len(df)
        
        print("\n✅ Cleaning Complete!")
        print("-" * 30)
        print(f"Initial Rows: {initial_rows}")
        print(f"Final Rows:   {final_rows}")
        print(f"Rows Removed: {initial_rows - final_rows}")
        print(f"Saved to:     {output_path}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_path}. Please check your raw data folder.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_nav_data()