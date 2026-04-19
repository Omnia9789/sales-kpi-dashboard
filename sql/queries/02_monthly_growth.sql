-- 02_monthly_growth.sql
-- Month-over-month revenue with growth rate.

WITH monthly AS (
    SELECT
        order_yearmonth,
        ROUND(SUM(sales), 2) AS revenue
    FROM sales
    GROUP BY order_yearmonth
),
with_lag AS (
    SELECT
        order_yearmonth,
        revenue,
        LAG(revenue) OVER (ORDER BY order_yearmonth) AS prev_revenue
    FROM monthly
)
SELECT
    order_yearmonth,
    revenue,
    prev_revenue,
    ROUND((revenue - prev_revenue) * 100.0 / NULLIF(prev_revenue, 0), 2) AS mom_growth_pct
FROM with_lag
ORDER BY order_yearmonth;
