from utils.db import get_engine
from etl.extract import extract
from etl.transform import transform

engine = get_engine()

df = extract()
dim_customer, dim_product, dim_date, fact_sales = transform(df)

dim_customer.to_sql("dim_customer", engine, if_exists="append", index=False)
dim_product.to_sql("dim_product", engine, if_exists="append", index=False)
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False)

print("ETL completed successfully")
