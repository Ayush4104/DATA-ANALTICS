"""Creates synthetic product-level promotion data -> data/promotions.csv"""
import numpy as np
import pandas as pd
import os

np.random.seed(7)
os.makedirs("data", exist_ok=True)
categories = {"Tshirts": 699, "Jeans": 1799, "Kurtas": 1299, "Dresses": 1999, "Sneakers": 2999}
margin_base = {"Tshirts": 0.50, "Jeans": 0.50, "Kurtas": 0.48, "Dresses": 0.52, "Sneakers": 0.55}

rows = []
for i in range(1, 3001):
    cat = np.random.choice(list(categories))
    mrp = categories[cat] * np.random.uniform(0.8, 1.2)
    disc = int(np.random.choice(range(0, 71, 5)))
    views = int(np.random.uniform(2000, 20000))
    # conversion rises with discount but flattens (diminishing returns) + noise
    conv = 0.012 + 0.030 * (1 - np.exp(-disc / 25)) + np.random.normal(0, 0.003)
    orders = int(views * max(conv, 0.002))
    rows.append([f"P{i:04d}", cat, round(mrp), disc, views, orders, round(mrp * (1 - margin_base[cat]))])

df = pd.DataFrame(rows, columns=["product_id", "category", "mrp", "discount_pct",
                                 "views", "orders", "cost_price"])
df.to_csv("data/promotions.csv", index=False)
print(f"Saved data/promotions.csv with {len(df):,} products")
