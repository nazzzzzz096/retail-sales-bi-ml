import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils.db import get_engine

engine = get_engine()

df = pd.read_sql(
    'SELECT customer_id, invoice_date, total_price, "InvoiceNo" FROM fact_sales',
    engine
)

snapshot = df["invoice_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg({
    "invoice_date": lambda x: (snapshot - x.max()).days,
    "InvoiceNo": "nunique",
    "total_price": "sum"
}).reset_index()

rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

X = StandardScaler().fit_transform(rfm[["recency", "frequency", "monetary"]])
rfm["segment"] = KMeans(n_clusters=4, random_state=42).fit_predict(X)

rfm.to_sql("customer_segments", engine, if_exists="replace", index=False)
