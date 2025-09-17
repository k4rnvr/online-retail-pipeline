SELECT p.description, SUM(f.quantity) AS total_sold
FROM fact_sales f
JOIN dim_product p ON f.stockcode = p.stockcode
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE EXTRACT(YEAR FROM f.invoicedate) = {YEAR} AND c.country IN ({COUNTRIES})
GROUP BY p.description
ORDER BY total_sold DESC
LIMIT 10;
