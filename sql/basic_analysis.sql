-- basic_analysis.sql
-- Basic aggregations on the sales table

-- 1. Total sales and profit
SELECT
    SUM(sales)   AS total_sales,
    SUM(profit)  AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_quantity
FROM sales;

-- 2. Average order value (AOV)
SELECT
    SUM(sales) / COUNT(DISTINCT order_id) AS average_order_value
FROM sales;

-- 3. Monthly sales totals
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(sales) AS monthly_sales,
    SUM(profit) AS monthly_profit,
    COUNT(DISTINCT order_id) AS orders_in_month
FROM sales
GROUP BY month
ORDER BY month;
