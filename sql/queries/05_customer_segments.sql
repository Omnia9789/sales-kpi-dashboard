-- 05_customer_segments.sql
-- Revenue and order count by customer segment.

SELECT
    segment,
    COUNT(DISTINCT customer_id)  AS unique_customers,
    COUNT(DISTINCT order_id)     AS total_orders,
    ROUND(SUM(sales),  2)        AS total_revenue,
    ROUND(AVG(sales),  2)        AS avg_order_value,
    ROUND(SUM(profit), 2)        AS total_profit
FROM sales
GROUP BY segment
ORDER BY total_revenue DESC;
