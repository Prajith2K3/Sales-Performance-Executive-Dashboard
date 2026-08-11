# Power BI Build Spec — Sales Performance Executive Dashboard

## 1. Power Query (M) Steps
1. Import `sales_orders.csv`
2. Change types: `order_date` → Date, `revenue`/`cost`/`profit`/`unit_price` → Decimal,
   `quantity` → Whole Number, `discount_pct` → Percentage
3. Add Column `Month` = `Date.StartOfMonth([order_date])`
4. Add Column `Fiscal Quarter` = `"Q" & Text.From(Date.QuarterOfYear([order_date])) & " " & Text.From(Date.Year([order_date]))`
5. Merge in a `DimDate` calendar table (CALENDAR(MIN(order_date), MAX(order_date))), mark as Date table

## 2. Data Model
Star schema: `stg_sales_orders` (fact) ← `DimDate`, plus `region`, `category`, `customer_type`
as flat dimension-like columns already denormalized in the fact for simplicity
(swap to `products`/`customers` dimension tables if importing the SQL schema).

## 3. DAX Measures
```dax
Total Revenue = SUM(stg_sales_orders[revenue])
Total Profit = SUM(stg_sales_orders[profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
Total Orders = DISTINCTCOUNT(stg_sales_orders[order_id])
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Revenue PM =
CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))

MoM Growth % =
DIVIDE([Total Revenue] - [Revenue PM], [Revenue PM], 0)

Revenue PY =
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))

YoY Growth % =
DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0)

Top Product Revenue Rank =
RANKX(ALL(stg_sales_orders[product_name]), CALCULATE([Total Revenue]))

Region Revenue Share % =
DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(stg_sales_orders[region])), 0)
```

## 4. Dashboard Pages

### Page 1 — Executive Dashboard
```
KPI Cards: Total Revenue | Total Profit | Margin % | YoY Growth | MoM Growth | AOV
Line chart: Monthly Revenue Trend (with YoY comparison line)
Bar chart: Revenue by Region
Donut: Revenue by Category
Slicers: Fiscal Quarter | Region | Category | Customer Type
```

### Page 2 — Sales Dashboard
```
Table: Order-level detail (order_id, date, product, customer, revenue, profit)
Bar: Top 10 Products by Revenue
Bar: Top 10 Customers by Revenue
KPI: Total Orders, AOV
```

### Page 3 — Regional Dashboard
```
Map/Bar: Revenue & Profit by Region
Matrix: Region x Category revenue heatmap
Slicer: Region
```

### Page 4 — Product Dashboard
```
Bar: Revenue & Margin % by Category
Table: Product-level revenue, units sold, margin %
Scatter: Unit Price vs Units Sold (bubble = revenue)
```

### Page 5 — Customer Dashboard
```
Bar: Revenue by Customer Type (Retail/Wholesale/Online)
Table: Top customers with AOV and order count
```

## 5. Drillthrough
- Drillthrough from any Region/Category bar → **Order Detail** page filtered to that
  selection, showing every order line.

## 6. Tooltip Pages
- Hover tooltip on Monthly Revenue Trend → shows Revenue, Profit, Margin %,
  MoM/YoY growth for that specific month.

## 7. Slicers (global)
Fiscal Quarter · Region · Category · Customer Type · Date Range
