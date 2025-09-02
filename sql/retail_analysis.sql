show databases;
create database data_analysis;

use data_analysis;

create table retail_sale (
	transactions_id INT,
    sale_date Date,
    sale_time Time,
    customer_id INT,
    gender VARCHAR(50),
    age INT,
    category VARCHAR(50),
    quantity INT,
    price_per_unit INT,
    cogs INT,
    total_sale INT
);

select * from retail_sale LIMIT 100;

select * from retail_sale WHERE category = 'Clothing' AND quantity > 4;

SELECT * FROM retail_sale WHERE category = 'Clothing' AND quantity > 4 AND MONTH(sale_date) = 11 AND YEAR(sale_date) = 2022;

SELECT customer_id, AVG(age) FROM retail_sale WHERE category = 'Beauty' GROUP BY customer_id;

SELECT AVG(age) AS avg_age
FROM retail_sale
WHERE category = 'Beauty';

SELECT CASE WHEN HOUR(sale_time) < 12 THEN 'MORNING' WHEN HOUR(sale_time) BETWEEN 12 AND 17 THEN 'Afternoon' ELSE 'Evening' END AS shift, COUNT(*) as total_orders FROM retail_sale GROUP BY shift;

SELECT category, COUNT(DISTINCT customer_id) AS count FROM retail_sale GROUP BY category;

SELECT * FROM retail_sale ORDER BY total_sale DESC LIMIT 5;
