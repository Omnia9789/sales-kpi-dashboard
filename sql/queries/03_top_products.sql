-- 03_top_products.sql
-- Top 10 products by total revenue.

SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales),    2) AS total_revenue,
    ROUND(SUM(profit),   2) AS total_profit,
    SUM(quantity)           AS units_sold
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 10;
