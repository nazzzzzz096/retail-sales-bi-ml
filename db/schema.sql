CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY,
    country TEXT
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id SERIAL PRIMARY KEY,
    stock_code TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    week INT,
    weekday_name TEXT,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS fact_sales (
    invoice_no TEXT,
    invoice_date TIMESTAMP,
    date_key DATE REFERENCES dim_date(date_key),
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    quantity INT,
    unit_price NUMERIC,
    total_price NUMERIC
);

