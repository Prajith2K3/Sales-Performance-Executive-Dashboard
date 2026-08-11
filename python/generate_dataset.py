"""
generate_dataset.py — Sales Performance Executive Dashboard
Generates 3 linked tables: orders (transaction line items), products, customers
Simulates a multi-region retail/distribution business over 3 fiscal years.
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta

np.random.seed(7)

# ---------------- Products ----------------
categories = {
    "Electronics": ["Wireless Earbuds", "Smart Watch", "Bluetooth Speaker", "Power Bank", "Laptop Stand"],
    "Home & Kitchen": ["Air Fryer", "Blender", "Cookware Set", "Vacuum Cleaner", "Coffee Maker"],
    "Apparel": ["Running Shoes", "Denim Jacket", "Backpack", "Sunglasses", "Wallet"],
    "Office Supplies": ["Ergonomic Chair", "Standing Desk", "Notebook Set", "Desk Organizer", "Monitor Arm"],
}
products = []
pid = 1
for cat, items in categories.items():
    for item in items:
        base_cost = np.random.uniform(8, 220)
        margin_pct = np.random.uniform(0.25, 0.55)
        unit_price = round(base_cost / (1 - margin_pct), 2)
        products.append({
            "product_id": f"P{pid:04d}", "product_name": item, "category": cat,
            "unit_cost": round(base_cost, 2), "unit_price": unit_price
        })
        pid += 1
products_df = pd.DataFrame(products)

# ---------------- Customers ----------------
regions = ["North", "South", "East", "West"]
n_customers = 400
customers = []
for i in range(1, n_customers + 1):
    customers.append({
        "customer_id": f"C{i:04d}",
        "customer_name": f"Customer_{i}",
        "region": np.random.choice(regions, p=[0.27, 0.24, 0.23, 0.26]),
        "customer_type": np.random.choice(["Retail", "Wholesale", "Online"], p=[0.45, 0.2, 0.35]),
    })
customers_df = pd.DataFrame(customers)

# ---------------- Orders (with seasonality + YoY growth) ----------------
start = date(2024, 1, 1)
end = date(2026, 7, 31)
days = (end - start).days
orders = []
order_id = 1

for d in range(days):
    current_date = start + timedelta(days=d)
    # seasonality: higher in Oct-Dec (festive/holiday), dip in Feb
    month = current_date.month
    seasonal_mult = {10: 1.4, 11: 1.5, 12: 1.6, 1: 0.9, 2: 0.75}.get(month, 1.0)
    # YoY growth ~12% per year
    year_mult = 1 + 0.12 * (current_date.year - 2024)
    n_orders_today = np.random.poisson(6 * seasonal_mult * year_mult)

    for _ in range(n_orders_today):
        cust = customers_df.sample(1).iloc[0]
        prod = products_df.sample(1).iloc[0]
        qty = np.random.randint(1, 8)
        discount_pct = np.random.choice([0, 0.05, 0.1, 0.15, 0.2], p=[0.4, 0.25, 0.2, 0.1, 0.05])
        unit_price = prod["unit_price"]
        revenue = round(unit_price * qty * (1 - discount_pct), 2)
        cost = round(prod["unit_cost"] * qty, 2)
        profit = round(revenue - cost, 2)

        orders.append({
            "order_id": f"O{order_id:06d}",
            "order_date": current_date.isoformat(),
            "customer_id": cust["customer_id"],
            "region": cust["region"],
            "customer_type": cust["customer_type"],
            "product_id": prod["product_id"],
            "product_name": prod["product_name"],
            "category": prod["category"],
            "quantity": qty,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
        })
        order_id += 1

orders_df = pd.DataFrame(orders)

orders_df.to_csv("/home/claude/sales-project/data/sales_orders.csv", index=False)
products_df.to_csv("/home/claude/sales-project/data/products.csv", index=False)
customers_df.to_csv("/home/claude/sales-project/data/customers.csv", index=False)

print("Orders:", len(orders_df))
print("Total revenue:", round(orders_df["revenue"].sum(), 2))
print("Total profit:", round(orders_df["profit"].sum(), 2))
print(orders_df.head(3).to_string())
