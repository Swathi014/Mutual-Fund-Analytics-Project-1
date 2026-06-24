# Bluestock Mutual Fund Analytics - Data Dictionary

## Overview
This document outlines the schema, column definitions, and data sources for the `bluestock_mf.db` SQLite database. The database follows a star schema design with one dimension table and three fact tables.

---

### 1. `dim_fund` (Dimension Table)
**Source:** `01_fund_master.csv`  
**Description:** Holds the static and descriptive metadata for each mutual fund scheme.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `amfi_code` | TEXT (PK) | Unique 6-digit identifier for the mutual fund scheme (AMFI standard). |
| `fund_house` | TEXT | The Asset Management Company (AMC) managing the fund (e.g., SBI, HDFC). |
| `scheme_name` | TEXT | The official, full name of the mutual fund scheme. |
| `category` | TEXT | Broad asset class category (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | Specific investment focus (e.g., Large Cap, Mid Cap, Liquid). |
| `risk_category` | TEXT | Risk profile defined by SEBI (e.g., Low, High, Very High). |
| `launch_date` | DATE | The inception date of the mutual fund scheme. |

---

### 2. `fact_nav` (Fact Table)
**Source:** `02_nav_history.csv`  
**Description:** Historical daily Net Asset Value (NAV) pricing data for the funds.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `amfi_code` | TEXT (FK) | Foreign key linking to `dim_fund`. |
| `nav_date` | DATE | The date of the quoted NAV price (YYYY-MM-DD format). |
| `nav` | REAL | The Net Asset Value price per unit on that specific date. |

---

### 3. `fact_transactions` (Fact Table)
**Source:** `08_investor_transactions.csv`  
**Description:** Log of individual investor transactions (inflows and outflows).

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `investor_id` | TEXT | Unique identifier for the individual investor. |
| `amfi_code` | TEXT (FK) | Foreign key linking to `dim_fund`. |
| `transaction_date` | DATE | The date the transaction was executed. |
| `transaction_type` | TEXT | Standardized type of transaction (`SIP`, `LUMPSUM`, or `REDEMPTION`). |
| `amount_inr` | REAL | Total monetary value of the transaction in Indian Rupees (₹). |
| `state` | TEXT | The Indian state where the investor resides. |
| `city` | TEXT | The city where the investor resides. |
| `city_tier` | TEXT | City classification tier (e.g., T30, B30). |
| `age_group` | TEXT | Age bracket of the investor (e.g., 18-25, 36-45). |
| `gender` | TEXT | Gender of the investor. |
| `annual_income_lakh` | REAL | Investor's self-reported annual income in Lakhs. |
| `payment_mode` | TEXT | Method used for the transaction (e.g., UPI, Net Banking). |
| `kyc_status` | TEXT | Investor's Know Your Customer (KYC) verification status. |

---

### 4. `fact_performance` (Fact Table)
**Source:** `07_scheme_performance.csv`  
**Description:** Pre-calculated return metrics and risk ratios for the funds.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `amfi_code` | TEXT (PK, FK) | Primary key, also a Foreign key linking to `dim_fund`. |
| `return_1yr` | REAL | The rolling 1-year annualized return percentage. |
| `return_3yr` | REAL | The rolling 3-year annualized return percentage. |
| `expense_ratio_pct` | REAL | The Total Expense Ratio (TER) charged by the fund, expressed as a percentage. |
| `sharpe_ratio` | REAL | Risk-adjusted return metric. Higher is better. |
| `is_negative_sharpe` | BOOLEAN | Flag (1/0 or True/False) indicating if the Sharpe ratio is below zero. |