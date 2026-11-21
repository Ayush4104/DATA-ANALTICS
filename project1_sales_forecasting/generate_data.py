"""Creates a realistic fashion e-commerce orders dataset (synthetic) -> data/orders.csv"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
os.makedirs("data", exist_ok=True)

categories = {
    "Men - Tshirts":   (699, 0.45), "Men - Jeans":    (1799, 0.50),
    "Women - Kurtas":  (1299, 0.48), "Women - Dresses": (1999, 0.52),
    "Footwear - Sneakers": (2999, 0.55), "Accessories - Watches": (3499, 0.50),
}
brands = ["Roadster", "HRX", "Libas", "Nike", "Puma", "Fossil", "H&M", "Biba"]

# monthly demand multiplier: festive (Oct-Nov), end-of-season sale (Jun, Dec), slow Feb/Aug
season = {1: 1.0, 2: 0.8, 3: 0.9, 4: 0.95, 5: 1.0, 6: 1.2,
          7: 0.9, 8: 0.85, 9: 1.0, 10: 1.6, 11: 1.8, 12: 1.3}

dates = pd.date_range("2024-01-01", "2025-12-31")
rows = []
for d in dates:
    growth = 1 + 0.35 * (d - dates[0]).days / len(dates)       # business grows over time
    n_orders = int(np.random.poisson(60 * season[d.month] * growth))
    for _ in range(n_orders):
        cat = np.random.choice(list(categories))
        mrp, margin = categories[cat]
        mrp = mrp * np.random.uniform(0.8, 1.2)
        disc = np.random.choice([0, 10, 20, 30, 40, 50],
                                p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.10])
        if d.month in (10, 11):                                   # festive -> deeper discounts
            disc = min(60, disc + 10)
        rows.append([d, np.random.randint(1, 4000), cat, np.random.choice(brands),
                     round(mrp), disc, np.random.choice([1, 1, 1, 2, 3]),
                     round(mrp * (1 - margin))])                  # cost price

df = pd.DataFrame(rows, columns=["order_date", "customer_id", "category", "brand",
                                 "mrp", "discount_pct", "quantity", "cost_price"])
df.insert(0, "order_id", range(1, len(df) + 1))
df.to_csv("data/orders.csv", index=False)
print(f"Saved data/orders.csv with {len(df):,} orders")
