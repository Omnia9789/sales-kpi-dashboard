-- 04_category_breakdown.sql
-- Revenue, profit, and margin by category and sub-category.

SELECT
    category,
    sub_category,
    ROUND(SUM(sales),  2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(discount) * 100, 2)  AS avg_discount_pct,
    ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM sales
GROUP BY category, sub_category
ORDER BY category, total_revenue DESC;
