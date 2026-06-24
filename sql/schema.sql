-- 1. Dimension Table: Fund Master
-- Holds the static/descriptive data about each mutual fund scheme
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    risk_category TEXT,
    launch_date DATE
);

-- 2. Fact Table: NAV History
-- Holds the daily pricing (Net Asset Value) for the funds
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code TEXT,
    nav_date DATE,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- 3. Fact Table: Investor Transactions
-- Holds the records of individual SIPs and Lumpsum investments
CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id TEXT,
    amfi_code TEXT,
    transaction_date DATE,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- 4. Fact Table: Scheme Performance
-- Holds the calculated return metrics and risk ratios
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code TEXT PRIMARY KEY,
    return_1yr REAL,
    return_3yr REAL,
    expense_ratio_pct REAL,
    sharpe_ratio REAL,
    is_negative_sharpe BOOLEAN,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);