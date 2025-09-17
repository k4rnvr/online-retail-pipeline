SELECT ROUND(SUM(total_amount)::NUMERIC / COUNT(DISTINCT invoice), 2) AS avg_order_value
FROM fact_sales;