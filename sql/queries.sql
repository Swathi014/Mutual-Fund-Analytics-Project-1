-- ============================================================================
-- TASK 6: 10 ANALYTICAL SQL QUERIES
-- ============================================================================

-- 1. Top 5 funds by Total Inflow Volume (Proxy for AUM)
SELECT d.scheme_name, SUM(t.amount_inr) as total_inflow
FROM fact_transactions t
JOIN dim_fund d ON t.amfi_code = d.amfi_code
GROUP BY d.scheme_name
ORDER BY total_inflow DESC
LIMIT 5;

-- 2. Average NAV per month across all records
SELECT strftime('%Y-%m', nav_date) as month, ROUND(AVG(nav), 2) as avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. Total SIP Inflows by Year (YoY Growth proxy)
SELECT strftime('%Y', transaction_date) as year, SUM(amount_inr) as total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

-- 4. Total Transaction Volume by State
SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_volume
FROM fact_transactions
GROUP BY state
ORDER BY total_volume DESC;

-- 5. Funds with extremely low expense ratios (< 1.0%)
SELECT d.scheme_name, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund d ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;

-- 6. Top 5 Best Performing Funds (by 1-Year Return)
SELECT d.scheme_name, p.return_1yr
FROM fact_performance p
JOIN dim_fund d ON p.amfi_code = d.amfi_code
ORDER BY p.return_1yr DESC
LIMIT 5;

-- 7. Average Expense Ratio by Fund Category
SELECT d.category, ROUND(AVG(p.expense_ratio_pct), 2) as avg_expense_ratio
FROM dim_fund d
JOIN fact_performance p ON d.amfi_code = p.amfi_code
GROUP BY d.category
ORDER BY avg_expense_ratio DESC;

-- 8. Transaction breakdown by City Tier
SELECT city_tier, COUNT(*) as transaction_count, SUM(amount_inr) as total_volume
FROM fact_transactions
GROUP BY city_tier
ORDER BY total_volume DESC;

-- 9. Fund Houses with the most 'Negative Sharpe Ratio' funds
SELECT d.fund_house, COUNT(*) as underperforming_funds
FROM dim_fund d
JOIN fact_performance p ON d.amfi_code = p.amfi_code
WHERE p.is_negative_sharpe = 1
GROUP BY d.fund_house
ORDER BY underperforming_funds DESC;

-- 10. Best Performing "Low Risk" Funds (3-Year Return)
SELECT d.scheme_name, d.risk_category, p.return_3yr
FROM dim_fund d
JOIN fact_performance p ON d.amfi_code = p.amfi_code
WHERE d.risk_category LIKE '%Low%'
ORDER BY p.return_3yr DESC
LIMIT 5;