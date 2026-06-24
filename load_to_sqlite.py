import pandas as pd
from sqlalchemy import create_engine, text
import os

def load_data_to_sqlite():
    db_path = 'bluestock_mf.db'
    schema_path = 'sql/schema.sql'
    engine = create_engine(f'sqlite:///{db_path}')
    
    print("=" * 60)
    print("🚀 TASK 5: LOADING CLEANED DATA INTO SQLITE")
    print("=" * 60)
    
    # --- Step 1: Initialize the Database Schema ---
    print("Initializing database tables from schema.sql...")
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema DDL statements split by semicolon
        with engine.begin() as conn:
            for statement in schema_sql.split(';'):
                if statement.strip():
                    conn.execute(text(statement))
        print("✅ Database tables structured successfully.")
    else:
        print(f"❌ Error: {schema_path} not found. Please create your schema file first.")
        return

    # --- Step 2: Load and Prepare Datasets ---
    try:
        print("\nReading and mapping datasets...")
        
        # 1. Dimension Fund Table (Using columns identified during Day 1 EDA)
        df_master = pd.read_csv('data/raw/01_fund_master.csv')
        dim_fund_cols = ['amfi_code', 'fund_house', 'scheme_name', 'category', 'sub_category', 'risk_category', 'launch_date']
        # Filter for only the columns defined in the SQLite schema
        df_dim_fund = df_master[[col for col in dim_fund_cols if col in df_master.columns]].drop_duplicates()

        # 2. Fact NAV Table
        df_nav = pd.read_csv('data/processed/clean_nav.csv')
        # Rename 'date' to 'nav_date' to match the database schema column name perfectly
        if 'date' in df_nav.columns:
            df_nav = df_nav.rename(columns={'date': 'nav_date'})

        # 3. Fact Transactions Table
        df_trans = pd.read_csv('data/processed/clean_transactions.csv')
        if 'date' in df_trans.columns:
            df_trans = df_trans.rename(columns={'date': 'transaction_date'})

        # 4. Fact Performance Table
        df_perf = pd.read_csv('data/processed/clean_performance.csv')
        # Ensure only schema-relevant columns are sent
        perf_cols = ['amfi_code', 'return_1yr', 'return_3yr', 'expense_ratio_pct', 'sharpe_ratio', 'is_negative_sharpe']
        df_fact_perf = df_perf[[col for col in perf_cols if col in df_perf.columns]]

        # --- Step 3: Write DataFrames to SQLite Tables ---
        print("\nWriting data to SQLite tables (if_exists='append')...")
        
        # Append data to tables. (Using chunksize helps manage memory for larger files like NAV history)
        df_dim_fund.to_sql('dim_fund', engine, if_exists='append', index=False)
        print(f"  -> Successfully loaded {len(df_dim_fund)} rows into 'dim_fund'")
        
        df_nav.to_sql('fact_nav', engine, if_exists='append', index=False, chunksize=10000)
        print(f"  -> Successfully loaded {len(df_nav)} rows into 'fact_nav'")
        
        df_trans.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"  -> Successfully loaded {len(df_trans)} rows into 'fact_transactions'")
        
        df_fact_perf.to_sql('fact_performance', engine, if_exists='append', index=False)
        print(f"  -> Successfully loaded {len(df_fact_perf)} rows into 'fact_performance'")
        
        print("\n🎉 Database pipeline complete! 'bluestock_mf.db' is fully populated.")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"❌ Data loading failed: {e}. Please ensure you ran all cleaning scripts first.")
    except Exception as e:
        print(f"❌ An unexpected database error occurred: {e}")

if __name__ == "__main__":
    load_data_to_sqlite()