SELECT 
    EXTRACT(MONTH FROM f.invoicedate) AS month,
    SUM(f.total_amount) AS monthly_sales
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE EXTRACT(YEAR FROM f.invoicedate) = {YEAR} AND c.country IN ({COUNTRIES})
GROUP BY month
ORDER BY month;
