# Project 2: Discount & Promotion Effectiveness Analysis

## Problem
Deeper discounts bring more orders, but do they bring more profit?
This project finds the discount level that maximises profit per product view, not just conversion.

## Tools
Python, Pandas, Matplotlib

## How to run
```
pip install -r requirements.txt
python generate_data.py     # creates data/promotions.csv (3,000 products)
python analysis.py          # prints insights, saves charts + CSVs in outputs/
```

## What it does
1. Computes conversion %, revenue, profit, and profit per view for each product
2. Groups products into discount bands (0-10%, 11-20% ... 51-70%)
3. Compares conversion vs profit per band
4. Finds the best discount band for each category
5. Plots the diminishing returns of discounting

## Key insights found
- Conversion keeps rising with discount (correlation 0.89), but with diminishing returns
- Profit per view peaks at 11-20% discount and turns negative above 50%
- The 11-20% band is the best for every category in this dataset

## Resume bullets (pick 2-3)
- Analyzed discount vs conversion on 3,000 products in Python to evaluate promotion effectiveness
- Showed that deep discounts (50%+) lift conversion but reduce profit; recommended a 11-20% sweet spot
- Built a profit-per-view metric and category-wise discount recommendations to balance topline and margin

## 30-second explanation for interviews
"I wanted to see whether bigger discounts actually help the business. I grouped products by discount band
and compared conversion with profit per view. Conversion rises with discount, but profit peaks at a moderate
discount and drops sharply at deep discounts, so I recommended a target band per category."

## Note
The dataset is synthetic so the project runs anywhere. Replace it with a real promotions or sales dataset
for a stronger portfolio version.
