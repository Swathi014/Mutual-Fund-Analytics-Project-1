import pandas as pd
import os
import glob

def inspect_datasets(data_dir="data/raw"):
    """
    Loads all CSV files from the specified directory and prints 
    their shape, data types, and the first 5 rows.
    """
    # Find all CSV files in the target directory
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in '{data_dir}'. Please ensure your 10 datasets are placed there.")
        return

    print(f"Found {len(csv_files)} datasets. Beginning inspection...\n")
    print("=" * 60)

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"--- Loading: {file_name} ---")
        
        try:
            # Load the dataset
            df = pd.read_csv(file_path)
            
            # Print Shape
            print(f"\n1. Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Print Data Types
            print("\n2. Data Types:")
            print(df.dtypes)
            
            # Print Head
            print("\n3. First 5 Rows:")
            # Displaying all columns for a better view in terminal
            pd.set_option('display.max_columns', None) 
            print(df.head())
            
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    # Ensure this points to the correct relative path based on where you run the script
    inspect_datasets(data_dir="data/raw")