import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.5)
ax.axis("off")

def draw_table(x, y, w, h, title, fields, color="#2563eb"):
    ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                 linewidth=1.5, edgecolor=color, facecolor="white"))
    ax.add_patch(patches.FancyBboxPatch((x, y+h-0.5), w, 0.5, boxstyle="round,pad=0.02",
                 linewidth=1.5, edgecolor=color, facecolor=color))
    ax.text(x + w/2, y + h - 0.25, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white")
    for i, f in enumerate(fields):
        ax.text(x + 0.15, y + h - 0.8 - i*0.32, f, ha="left", va="center", fontsize=9)

draw_table(0.3, 1.5, 2.6, 2.2, "customers", [
    "PK  customer_id", "    customer_name", "    region", "    customer_type"
], color="#16a34a")

draw_table(3.6, 0.5, 3.0, 4.2, "order_lines", [
    "PK  order_id", "    order_date", "FK  customer_id", "FK  product_id",
    "    quantity", "    discount_pct", "    revenue", "    cost", "    profit"
])

draw_table(7.2, 1.5, 2.5, 2.2, "products", [
    "PK  product_id", "    product_name", "    category", "    unit_cost", "    unit_price"
], color="#16a34a")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#64748b", lw=1.5))

arrow(2.9, 2.6, 3.6, 2.6)
arrow(6.6, 2.6, 7.2, 2.6)

ax.set_title("Sales Performance Dashboard — Entity Relationship Diagram", fontsize=15, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("/home/claude/sales-project/images/er_diagram.png", dpi=150)
plt.close()
print("ER diagram saved")
