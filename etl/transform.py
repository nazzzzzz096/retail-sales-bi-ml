import pandas as pd

def transform(df):
    df = df.dropna(subset=["CustomerID"])
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    dim_customer = df.groupby("CustomerID")["Country"].first().reset_index()

    dim_product = df[["StockCode", "Description"]].drop_duplicates().reset_index(drop=True)
    dim_product["product_id"] = dim_product.index + 1

    df = df.merge(dim_product, on=["StockCode", "Description"])

    dim_date = pd.DataFrame(df["InvoiceDate"].dt.date.unique(), columns=["date_key"])
    dim_date["day"] = pd.to_datetime(dim_date["date_key"]).dt.day
    dim_date["month"] = pd.to_datetime(dim_date["date_key"]).dt.month
    dim_date["year"] = pd.to_datetime(dim_date["date_key"]).dt.year
    dim_date["week"] = pd.to_datetime(dim_date["date_key"]).dt.isocalendar().week
    dim_date["weekday_name"] = pd.to_datetime(dim_date["date_key"]).dt.day_name()
    dim_date["is_weekend"] = dim_date["weekday_name"].isin(["Saturday", "Sunday"])

    fact_sales = df[[
        "InvoiceNo", "InvoiceDate", "CustomerID",
        "product_id", "Quantity", "UnitPrice", "TotalPrice"
    ]]
    fact_sales.rename(columns={
        "InvoiceDate": "invoice_date",
        "CustomerID": "customer_id",
        "Quantity": "quantity",
        "UnitPrice": "unit_price",
        "TotalPrice": "total_price"
    }, inplace=True)
    fact_sales["date_key"] = fact_sales["invoice_date"].dt.date

    return dim_customer, dim_product, dim_date, fact_sales

