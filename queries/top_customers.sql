SELECT c.customer_id, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE EXTRACT(YEAR FROM f.invoicedate) = {YEAR} AND c.country IN ({COUNTRIES})
GROUP BY c.customer_id
ORDER BY revenue DESC
LIMIT 10;
