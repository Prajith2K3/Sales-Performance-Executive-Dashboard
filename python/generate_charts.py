import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({"font.size": 11, "figure.dpi": 150})
COLORS = ["#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed"]

df = pd.read_csv("/home/claude/sales-project/data/sales_orders.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

# 1. Monthly revenue trend
fig, ax = plt.subplots(figsize=(9, 4.5))
monthly = df.groupby("month")["revenue"].sum()
ax.plot(monthly.index, monthly.values, linewidth=2.5, color=COLORS[0], marker="o", markersize=4)
ax.fill_between(monthly.index, monthly.values, alpha=0.12, color=COLORS[0])
ax.set_ylabel("Revenue ($)")
ax.set_title("Monthly Revenue Trend (2024-2026)", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45, ha="right")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/monthly_revenue_trend.png")
plt.close()

# 2. Revenue by region
fig, ax = plt.subplots(figsize=(7, 4.5))
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
bars = ax.bar(region_rev.index, region_rev.values / 1000, color=COLORS[:len(region_rev)])
ax.set_ylabel("Revenue ($ thousands)")
ax.set_title("Total Revenue by Region", fontsize=14, fontweight="bold")
for b, v in zip(bars, region_rev.values):
    ax.text(b.get_x() + b.get_width()/2, v/1000 + 15, f"${v/1000:.0f}K", ha="center", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/revenue_by_region.png")
plt.close()

# 3. Margin by category
fig, ax = plt.subplots(figsize=(7, 4.5))
cat = df.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
cat["margin_pct"] = 100 * cat["profit"] / cat["revenue"]
cat = cat.sort_values("margin_pct", ascending=False)
bars = ax.bar(cat.index, cat["margin_pct"], color=COLORS[:len(cat)])
ax.set_ylabel("Profit Margin (%)")
ax.set_title("Profit Margin by Product Category", fontsize=14, fontweight="bold")
for b, v in zip(bars, cat["margin_pct"]):
    ax.text(b.get_x() + b.get_width()/2, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/margin_by_category.png")
plt.close()

# 4. Top 10 products
fig, ax = plt.subplots(figsize=(8, 5))
top = df.groupby("product_name")["revenue"].sum().sort_values(ascending=True).tail(10)
bars = ax.barh(top.index, top.values / 1000, color=COLORS[0])
ax.set_xlabel("Revenue ($ thousands)")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/top_10_products.png")
plt.close()

# 5. Seasonality heatmap-style bar (avg revenue by month-of-year)
fig, ax = plt.subplots(figsize=(8, 4.5))
df["month_name"] = df["order_date"].dt.strftime("%b")
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
seasonal = df.groupby("month_name")["revenue"].mean().reindex(month_order)
colors = ["#dc2626" if m in ["Oct","Nov","Dec"] else "#2563eb" for m in month_order]
ax.bar(seasonal.index, seasonal.values, color=colors)
ax.set_ylabel("Avg Revenue per Order Day ($)")
ax.set_title("Seasonality: Avg Daily Revenue by Month (Red = Festive Season)", fontsize=13, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/seasonality_by_month.png")
plt.close()

print("Generated 5 charts for sales project")
