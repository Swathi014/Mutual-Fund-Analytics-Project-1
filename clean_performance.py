import pandas as pd
import numpy as np
import os

def clean_performance():
    # Using the file name from your Day 1 Explorer screenshot
    input_path = 'data/raw/07_scheme_performance.csv'
    output_path = 'data/processed/clean_performance.csv'
    
    print("=" * 50)
    print("🧹 TASK 3: CLEANING SCHEME PERFORMANCE")
    print("=" * 50)
    
    try:
        # 1. Load the dataset
        print(f"Loading {input_path}...")
        df = pd.read_csv(input_path)
        initial_rows = len(df)
        
        # 2. Validate return values are numeric
        print("Validating return values are numeric...")
        # Automatically find columns related to 'return' (e.g., 1yr_return, 3yr_return)
        return_cols = [col for col in df.columns if 'return' in col.lower()]
        for col in return_cols:
            # Coerce errors to NaN so we don't have stray string characters breaking math later
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # 3. Flag negative Sharpe ratios
        print("Flagging negative Sharpe ratios...")
        sharpe_col = 'sharpe_ratio' if 'sharpe_ratio' in df.columns else None
        if sharpe_col:
            df[sharpe_col] = pd.to_numeric(df[sharpe_col], errors='coerce')
            # Create a boolean flag column: True if negative, False otherwise
            df['is_negative_sharpe'] = df[sharpe_col] < 0
            num_negative = df['is_negative_sharpe'].sum()
            print(f"  -> Flagged {num_negative} funds with negative Sharpe ratios.")
            
        # 4. Check expense_ratio range (0.1% - 2.5%)
        print("Validating expense ratio range (0.1% to 2.5%)...")
        # Handle potential column name variations
        expense_col = None
        if 'expense_ratio_pct' in df.columns:
            expense_col = 'expense_ratio_pct'
        elif 'expense_ratio' in df.columns:
            expense_col = 'expense_ratio'
            
        if expense_col:
            df[expense_col] = pd.to_numeric(df[expense_col], errors='coerce')
            # Create a mask for valid ranges and filter the dataframe
            valid_er_mask = (df[expense_col] >= 0.1) & (df[expense_col] <= 2.5)
            invalid_er_count = len(df) - valid_er_mask.sum()
            
            if invalid_er_count > 0:
                print(f"  -> Dropping {invalid_er_count} rows with invalid expense ratios.")
                df = df[valid_er_mask]
        else:
            print("  -> No expense ratio column found to validate.")

        # 5. Save to processed folder
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv(output_path, index=False)
        
        final_rows = len(df)
        
        print("\n✅ Task 3 Complete!")
        print("-" * 30)
        print(f"Initial Rows: {initial_rows}")
        print(f"Final Rows:   {final_rows}")
        print(f"Rows Removed: {initial_rows - final_rows}")
        print(f"Saved to:     {output_path}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_path}.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_performance()