SELECT DISTINCT EXTRACT(YEAR FROM invoicedate) AS year
FROM fact_sales
ORDER BY year;
