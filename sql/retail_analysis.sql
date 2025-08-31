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
