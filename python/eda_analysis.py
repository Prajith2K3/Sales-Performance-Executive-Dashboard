"""
eda_analysis.py — Sales Performance Executive Dashboard
Loads sales_orders.csv, computes KPIs, growth rates, and top performers.
"""
import json
import pandas as pd

df = pd.read_csv("/home/claude/sales-project/data/sales_orders.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# ---------------- Headline KPIs ----------------
total_revenue = round(df["revenue"].sum(), 2)
total_profit = round(df["profit"].sum(), 2)
margin_pct = round(100 * total_profit / total_revenue, 2)
total_orders = df["order_id"].nunique()
aov = round(total_revenue / total_orders, 2)

kpis = {
    "total_revenue": total_revenue,
    "total_profit": total_profit,
    "profit_margin_pct": margin_pct,
    "total_orders": int(total_orders),
    "average_order_value": aov,
}
with open("/home/claude/sales-project/data/sales_kpis.json", "w") as f:
    json.dump(kpis, f, indent=2)

print("=== HEADLINE KPIs ===")
for k, v in kpis.items():
    print(f"{k}: {v}")

# ---------------- MoM / YoY growth ----------------
monthly = df.groupby("month")["revenue"].sum().reset_index()
monthly["mom_growth_pct"] = (monthly["revenue"].pct_change() * 100).round(2)
monthly["yoy_growth_pct"] = (monthly["revenue"].pct_change(12) * 100).round(2)
print("\n=== Monthly Revenue & Growth (last 6 months) ===")
print(monthly.tail(6).to_string(index=False))

# ---------------- Region / Category performance ----------------
print("\n=== Revenue & Margin by Region ===")
region_stats = df.groupby("region").agg(revenue=("revenue","sum"), profit=("profit","sum"))
region_stats["margin_pct"] = (100 * region_stats["profit"] / region_stats["revenue"]).round(2)
print(region_stats.sort_values("revenue", ascending=False).round(2))

print("\n=== Revenue & Margin by Category ===")
cat_stats = df.groupby("category").agg(revenue=("revenue","sum"), profit=("profit","sum"))
cat_stats["margin_pct"] = (100 * cat_stats["profit"] / cat_stats["revenue"]).round(2)
print(cat_stats.sort_values("revenue", ascending=False).round(2))

# ---------------- Top products / customers ----------------
print("\n=== Top 5 Products by Revenue ===")
print(df.groupby("product_name")["revenue"].sum().sort_values(ascending=False).head(5).round(2))

print("\n=== Top 5 Customers by Revenue ===")
print(df.groupby("customer_id")["revenue"].sum().sort_values(ascending=False).head(5).round(2))

monthly.to_csv("/home/claude/sales-project/data/monthly_revenue_growth.csv", index=False)
