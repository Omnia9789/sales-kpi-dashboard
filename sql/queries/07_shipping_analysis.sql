-- 07_shipping_analysis.sql
-- Revenue, profit, and order count by ship mode.

SELECT
    ship_mode,
    COUNT(DISTINCT order_id)   AS total_orders,
    ROUND(SUM(sales),  2)      AS total_revenue,
    ROUND(SUM(profit), 2)      AS total_profit,
    ROUND(AVG(
        JULIANDAY(ship_date) - JULIANDAY(order_date)
    ), 1)                      AS avg_days_to_ship
FROM sales
GROUP BY ship_mode
ORDER BY total_revenue DESC;
