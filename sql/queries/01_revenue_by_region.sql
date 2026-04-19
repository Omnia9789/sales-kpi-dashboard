-- 01_revenue_by_region.sql
-- Total revenue and profit by region, ranked highest first.

SELECT
    region,
    ROUND(SUM(sales),  2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;
