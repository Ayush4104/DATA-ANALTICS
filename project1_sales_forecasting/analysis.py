"""
Project 1: Fashion E-commerce Sales Analysis & Demand Forecasting
Steps: clean -> KPIs -> trends -> top categories/brands -> forecast next 6 months
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/orders.csv", parse_dates=["order_date"])

# ---------- 1. Feature engineering ----------
df["selling_price"] = df["mrp"] * (1 - df["discount_pct"] / 100)
df["revenue"] = df["selling_price"] * df["quantity"]
df["profit"] = (df["selling_price"] - df["cost_price"]) * df["quantity"]
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

# ---------- 2. Key business metrics ----------
kpis = {
    "Total Orders": len(df),
    "Total Revenue (Rs)": round(df["revenue"].sum()),
    "Total Profit (Rs)": round(df["profit"].sum()),
    "Gross Margin %": round(df["profit"].sum() / df["revenue"].sum() * 100, 1),
    "Average Order Value (Rs)": round(df["revenue"].mean()),
    "Unique Customers": df["customer_id"].nunique(),
}
print("\n=== KEY METRICS ===")
for k, v in kpis.items():
    print(f"{k}: {v:,}")
pd.Series(kpis).to_csv("outputs/kpis.csv", header=["value"])

# ---------- 3. Category & brand performance ----------
cat = df.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum"),
                                 orders=("order_id", "count"))
cat["margin_%"] = (cat["profit"] / cat["revenue"] * 100).round(1)
cat = cat.sort_values("revenue", ascending=False)
print("\n=== CATEGORY PERFORMANCE ===\n", cat.round(0))
cat.to_csv("outputs/category_performance.csv")

brand = df.groupby("brand")["revenue"].sum().sort_values(ascending=False)

# ---------- 4. Monthly trend ----------
monthly = df.groupby("month")["revenue"].sum()

# ---------- 5. Forecast: linear trend + month-of-year seasonality ----------
m = monthly.reset_index()
m["t"] = np.arange(len(m))
m["moy"] = m["month"].dt.month
X = pd.concat([m[["t"]], pd.get_dummies(m["moy"], prefix="m", drop_first=True)], axis=1).astype(float)
model = LinearRegression().fit(X, m["revenue"])

# hold-out check: train on first 18 months, test on last 6
tr, te = slice(0, 18), slice(18, 24)
chk = LinearRegression().fit(X.iloc[tr], m["revenue"].iloc[tr])
pred = chk.predict(X.iloc[te])
mape = np.mean(np.abs((m["revenue"].iloc[te] - pred) / m["revenue"].iloc[te])) * 100
print(f"\nBack-test MAPE on last 6 months: {mape:.1f}%")

future_months = pd.date_range(m["month"].iloc[-1] + pd.offsets.MonthBegin(1), periods=6, freq="MS")
fut = pd.DataFrame({"month": future_months})
fut["t"] = np.arange(len(m), len(m) + 6)
fut["moy"] = fut["month"].dt.month
Xf = pd.concat([fut[["t"]], pd.get_dummies(fut["moy"], prefix="m")], axis=1)
Xf = Xf.reindex(columns=X.columns, fill_value=0).astype(float)
fut["forecast_revenue"] = model.predict(Xf)
print("\n=== 6-MONTH FORECAST ===\n", fut.assign(forecast_revenue=fut["forecast_revenue"].round(0))[["month", "forecast_revenue"]].to_string(index=False))
fut[["month", "forecast_revenue"]].to_csv("outputs/forecast.csv", index=False)

# ---------- 6. Charts ----------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly.index, monthly / 1e6, marker="o", label="Actual")
ax.plot(fut["month"], fut["forecast_revenue"] / 1e6, marker="o", linestyle="--", color="orange", label="Forecast")
ax.set_title("Monthly Revenue: Actual vs 6-Month Forecast"); ax.set_ylabel("Revenue (Rs million)")
ax.legend(); ax.grid(alpha=.3); plt.tight_layout(); plt.savefig("outputs/revenue_forecast.png", dpi=150); plt.close()

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
(cat["revenue"] / 1e6).plot.barh(ax=ax[0], color="#ff3f6c"); ax[0].invert_yaxis()
ax[0].set_title("Revenue by Category (Rs million)")
cat["margin_%"].plot.barh(ax=ax[1], color="#f39c12"); ax[1].invert_yaxis()
ax[1].set_title("Gross Margin % by Category")
plt.tight_layout(); plt.savefig("outputs/category_performance.png", dpi=150); plt.close()

(brand / 1e6).plot.bar(figsize=(9, 5), color="#5b4cb3")
plt.title("Revenue by Brand (Rs million)"); plt.ylabel("Rs million"); plt.tight_layout()
plt.savefig("outputs/brand_revenue.png", dpi=150); plt.close()

print("\nCharts and CSVs saved in outputs/")
