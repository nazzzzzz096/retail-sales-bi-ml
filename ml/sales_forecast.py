import pandas as pd
from prophet import Prophet
from utils.db import get_engine

engine = get_engine()

df = pd.read_sql(
    "SELECT invoice_date, total_price FROM fact_sales",
    engine
)

daily = df.groupby(df["invoice_date"].dt.date)["total_price"].sum().reset_index()
daily.columns = ["ds", "y"]

model = Prophet()
model.fit(daily)

future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

forecast.to_sql("sales_forecast", engine, if_exists="replace", index=False)

