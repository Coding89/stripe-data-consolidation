"""
Stripe Financial Dashboard Engine:

Processes raw transactional parquet data to calculate net processing volume.
Generates three analytical Plotly visualisations:

1. Trend Analysis: A scatter graph showing monthly Gross Revenue vs. Net Income (Line/Area).
2. Revenue Predictability: Stacked breakdown of recurring vs. One time giving. A bar chart showcasing total baseline predictability.
3. Revenue Breakdown: A donut chart displaying the revenue breakdown by category with custom colors and radial percentage labels.

"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Loading filepath
df = pd.read_parquet("full_data.parquet")
df["created_utc"] = pd.to_datetime(df["created_utc"])
df = df.sort_values("created_utc")

#CSV imports often have integers (cents/pence etc). The lines below take these into account
df["amount"] = df["amount"] / 100
df["fee"] = df["fee"] / 100

#This calculates key finanical metrics
df["net_income"] = df["amount"] - df["fee"]
df["month"] = df["created_utc"].dt.to_period("M").astype(str)

rec_col = "payment_metadata[donorbox_recurring_donation]"
df[rec_col] = df[rec_col].fillna("One-time").replace({True: "Recurring", False: "One-time", "true": "Recurring", "false": "One-time"})

#Font styles
FONT_FAMILY = "Helvetica Neue, Helvetica, Arial, san-serif"
COLOR_GROSS = "#1B3E6F"
COLOR_NET = "#0AA094"
COLOR_RECURRING = "#1E5DE6"
COLOR_ONETIME = "#A0ACBE"
BG_COLOR = "#FFFFFF"

#Visualisation 1: The executive summary and donation trends. Monthly Gross Revenue vs. Net Income (Line/Area).

monthly = df.groupby("month")[["amount", "fee", "net_income"]].sum().reset_index()

fig_trend = go.Figure()

#Gross revenue area chart
fig_trend.add_trace(go.Scatter(
    x=monthly["month"], y=monthly["amount"], name="Gross Revenue",
    mode="lines", line=dict(color=COLOR_GROSS, width=3),
    fill="tozeroy", fillcolor="rgba(26, 54, 95, 0.04)"
))

#Net income line chart
fig_trend.add_trace(go.Scatter(
    x=monthly["month"], y=monthly["net_income"], name="Net Income (Post-fee)",
    mode="lines+markers", line=dict(color=COLOR_NET, width=4),
    marker=dict(size=8, symbol="circle")
))
# This applies custom typography, background theme, unfiied hover behaviour, and header layout to the trend chart.
fig_trend.update_layout(
    title=dict(text="<b>Financial Performance Overview</b><br><sup>Monthly Gross Revenue vs Net Processing Volume</sup>", font=dict(size=20, color="#0F172A")),
    font=dict(family=FONT_FAMILY, color="#263243"),
    plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=120, b=50, l=60, r=20)
)

fig_trend.update_xaxes(showgrid=False, tickangle=-45, linewidth=1, linecolor="#D8E3F0")
fig_trend.update_yaxes(showgrid=True, gridcolor="#E3EAF1", tickformat="$", linewidth=1, linecolor="#BDC9D7")

#Visualisation 2: Revenue Predictability

rec_summary = df.groupby(["month", rec_col])["amount"].sum().reset_index()

#creates a stacked bar chart analysing monthly recurring vs one time revenue streams
fig_mix = px.bar(
    rec_summary, x="month", y="amount", color=rec_col,
    title="<b>Revenue Predictability Analysis</b><br><sup>Monthly Distribution of Recurring vs. One-Time Streams</sup>",
    color_discrete_map={"Recurring": COLOR_RECURRING, "One-time": COLOR_ONETIME},
    category_orders={rec_col: ["Recurring", "One-time"]}
)

fig_mix.update_layout(
    font=dict(family=FONT_FAMILY, color="#3B4D67"),
    plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
    barmode="stack",
    legend=dict(title=None, orientation="h", yanchor="bottom", y=2.01, xanchor="right", x=1),
    margin=dict(t=120, b=50, l=60, r=20)
)

fig_mix.update_xaxes(showgrid=False, tickangle=-45, linewidth=1, linecolor="#3B4D67")
fig_mix.update_yaxes(showgrid=True, gridcolor="#F1F5F9")

#Visalisation 3: Cohort Mix (Donut)

total_summary = df.groupby(rec_col)["amount"].sum().reset_index()
#generates a donut chart displaying the revenue breakdown by category with custom colors and radial percentage labels.
fig_pie = go.Figure(data=[go.Pie(
    labels=total_summary[rec_col],
    values=total_summary["amount"],
    hole=0.5,
    marker=dict(colors=[COLOR_RECURRING, COLOR_ONETIME]),
    textinfo='percent+label',
    insidetextorientation='radial'
)])
# formatting layout
fig_pie.update_layout(
    title=dict(text="<b>Lifetime Funding Mix</b><br><sup>Proportion of Total Baseline Predictability</sup>", font=dict(size=18, color="#1B2B53")),
    font=dict(family=FONT_FAMILY),
    paper_bgcolor=BG_COLOR,
    margin=dict(t=100, b=40, l=40, r=40),
    showlegend=False
)
# print out script
if __name__ == "__main__":
    fig_trend.show()
    fig_mix.show()
    fig_pie.show()