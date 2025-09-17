SELECT
    SUM(f.total_amount) AS total_revenue,
    ROUND(SUM(f.total_amount)/NULLIF(COUNT(DISTINCT f.invoice),0),2) AS avg_order_value,
    COUNT(*) FILTER (WHERE f.is_cancelled = TRUE) AS cancelled_orders
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE EXTRACT(YEAR FROM f.invoicedate) = {YEAR} AND c.country IN ({COUNTRIES});
