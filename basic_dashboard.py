""""
Python script to create financial visual trends. 
The first is a line chart showing "monthly consolidated revenue trends" over the months and years.
The second is a pie chart that shows the distribution of currencies and amounts per currency.

The outputs are one line chart and one pie chart.

"""

import pandas as pd
import plotly.express as px

df = pd.read_parquet("full_data.parquet")

# Date format and sort chronologically
df["created_utc"] = pd.to_datetime(df["created_utc"])
df = df.sort_values("created_utc")

#cumulative transaction volumes by month
df["month"] = df["created_utc"].dt.to_period("M").astype(str)
monthly_summary = (
    df.groupby("month")[["amount", "fee"]].sum().reset_index()
)

#this creates an interactive time series chart
fig_trend = px.line(
    monthly_summary,
    x="month",
    y="amount",
    title="Stripe Monthly Consolidated Revenue Trend",
    labels={"month": "Month", "amount": "Total Revenue ($)"},
    markers=True
)
fig_trend.show()

#This creates a breakdown by currency or recurring donation status
fig_currency = px.pie(
    df,
    names="currency",
    values="amount",
    title="Revenue Distribution by Currency"
)
fig_currency.show()

