-- 08_anomaly_detection.sql
-- Orders where discount >= 40% AND profit is negative — potential pricing anomalies.

SELECT
    order_id,
    order_date,
    product_name,
    category,
    region,
    ROUND(sales,    2) AS sales,
    ROUND(profit,   2) AS profit,
    ROUND(discount * 100, 1) AS discount_pct
FROM sales
WHERE discount >= 0.40
  AND profit < 0
ORDER BY profit ASC
LIMIT 20;
