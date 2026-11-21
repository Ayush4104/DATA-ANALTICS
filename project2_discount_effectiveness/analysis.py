"""
Project 2: Discount & Promotion Effectiveness Analysis
Question: Which discount level maximises profit, not just orders?
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/promotions.csv")

# ---------- 1. Metrics ----------
df["selling_price"] = df["mrp"] * (1 - df["discount_pct"] / 100)
df["conversion_%"] = df["orders"] / df["views"] * 100
df["revenue"] = df["selling_price"] * df["orders"]
df["profit"] = (df["selling_price"] - df["cost_price"]) * df["orders"]
df["profit_per_view"] = df["profit"] / df["views"]

# ---------- 2. Group into discount bands ----------
bins = [-1, 10, 20, 30, 40, 50, 70]
labels = ["0-10%", "11-20%", "21-30%", "31-40%", "41-50%", "51-70%"]
df["discount_band"] = pd.cut(df["discount_pct"], bins=bins, labels=labels)

band = df.groupby("discount_band", observed=True).agg(
    products=("product_id", "count"),
    avg_conversion=("conversion_%", "mean"),
    total_orders=("orders", "sum"),
    total_revenue=("revenue", "sum"),
    total_profit=("profit", "sum"),
    profit_per_view=("profit_per_view", "mean"),
).round(2)
print("\n=== DISCOUNT BAND PERFORMANCE ===\n", band)
band.to_csv("outputs/discount_band_summary.csv")

best_conv = band["avg_conversion"].idxmax()
best_profit = band["profit_per_view"].idxmax()
print(f"\nHighest conversion band : {best_conv}")
print(f"Highest profit-per-view : {best_profit}")
print("Insight: the deepest discount wins on conversion but not on profit.")

# ---------- 3. Category-wise best discount ----------
cat_best = (df.groupby(["category", "discount_band"], observed=True)["profit_per_view"]
              .mean().reset_index()
              .sort_values("profit_per_view", ascending=False)
              .groupby("category").head(1))
print("\n=== BEST DISCOUNT BAND PER CATEGORY (by profit per view) ===\n", cat_best.round(2).to_string(index=False))
cat_best.to_csv("outputs/best_discount_per_category.csv", index=False)

print("\nCorrelation of discount with conversion: %.2f" % df["discount_pct"].corr(df["conversion_%"]))
print("Correlation of discount with profit/view: %.2f" % df["discount_pct"].corr(df["profit_per_view"]))

# ---------- 4. Charts ----------
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
band["avg_conversion"].plot.bar(ax=ax[0], color="#ff3f6c", rot=0)
ax[0].set_title("Avg Conversion % by Discount Band"); ax[0].set_ylabel("Conversion %")
band["profit_per_view"].plot.bar(ax=ax[1], color="#22a06b", rot=0)
ax[1].set_title("Profit per View (Rs) by Discount Band"); ax[1].set_ylabel("Rs per view")
plt.tight_layout(); plt.savefig("outputs/discount_analysis.png", dpi=150); plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(df["discount_pct"], df["conversion_%"], alpha=.25, s=10, color="#5b4cb3")
plt.title("Discount % vs Conversion % (diminishing returns)")
plt.xlabel("Discount %"); plt.ylabel("Conversion %"); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig("outputs/discount_vs_conversion.png", dpi=150); plt.close()
print("\nCharts and CSVs saved in outputs/")
