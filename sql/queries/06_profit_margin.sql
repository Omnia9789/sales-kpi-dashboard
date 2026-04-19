-- 06_profit_margin.sql
-- Products with negative profit margin (loss-makers), ordered by worst first.

SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales),  2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM sales
GROUP BY product_name, category, sub_category
HAVING profit_margin_pct < 0
ORDER BY profit_margin_pct ASC
LIMIT 15;
