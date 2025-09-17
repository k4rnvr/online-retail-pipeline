SELECT COUNT(*) AS cancelled_orders,
       SUM(total_amount) AS cancelled_revenue
FROM fact_sales
WHERE is_cancelled = TRUE;
