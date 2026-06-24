import pandas as pd
import os

def clean_transactions():
    # Using the file name from your Day 1 Explorer screenshot
    input_path = 'data/raw/08_investor_transactions.csv'
    output_path = 'data/processed/clean_transactions.csv'
    
    print("=" * 50)
    print("🧹 TASK 2: CLEANING INVESTOR TRANSACTIONS")
    print("=" * 50)
    
    try:
        # 1. Load the dataset
        print(f"Loading {input_path}...")
        df = pd.read_csv(input_path)
        initial_rows = len(df)
        
        # Define expected columns (Defensive coding in case of minor name variations)
        date_col = 'date' if 'date' in df.columns else 'transaction_date'
        type_col = 'transaction_type' if 'transaction_type' in df.columns else 'type'
        amt_col = 'amount'
        kyc_col = 'kyc_status'
        
        # 2. Fix date formats (Parse to datetime)
        print("Parsing dates to datetime...")
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col]) # Drop rows where date is completely invalid
        
        # 3. Standardize transaction_type (SIP/Lumpsum/Redemption)
        print("Standardizing transaction types...")
        if type_col in df.columns:
            # Strip whitespace and make uppercase
            df[type_col] = df[type_col].astype(str).str.strip().str.upper()
            
            # Map common variations to standard terms
            type_mapping = {
                'S.I.P': 'SIP',
                'S.I.P.': 'SIP',
                'LUMP SUM': 'LUMPSUM',
                'LUMP-SUM': 'LUMPSUM'
            }
            df[type_col] = df[type_col].replace(type_mapping)
        
        # 4. Validate amount > 0
        print("Filtering amounts > 0...")
        if amt_col in df.columns:
            # Coerce to numeric in case there are stray strings like '₹5000'
            df[amt_col] = pd.to_numeric(df[amt_col], errors='coerce')
            df = df[df[amt_col] > 0]
            
        # 5. Check KYC status values
        print("Cleaning KYC status...")
        if kyc_col in df.columns:
            df[kyc_col] = df[kyc_col].astype(str).str.strip().str.upper()
            
        # 6. Save to processed folder
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv(output_path, index=False)
        
        final_rows = len(df)
        
        print("\n✅ Task 2 Complete!")
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
    clean_transactions()