-- ============================================================
-- 02_analysis_queries.sql — Sales Performance Executive Dashboard
-- Staging table mirrors sales_orders.csv (denormalized for BI)
-- ============================================================

CREATE TABLE IF NOT EXISTS stg_sales_orders (
    order_id         VARCHAR(10),
    order_date        DATE,
    customer_id         VARCHAR(10),
    region                VARCHAR(20),
    customer_type           VARCHAR(20),
    product_id                VARCHAR(10),
    product_name                 VARCHAR(100),
    category                        VARCHAR(50),
    quantity                           INT,
    unit_price                            NUMERIC(10,2),
    discount_pct                             NUMERIC(4,2),
    revenue                                     NUMERIC(12,2),
    cost                                           NUMERIC(12,2),
    profit                                            NUMERIC(12,2)
);

-- ------------------------------------------------------------
-- 1. Headline KPIs: Revenue, Profit, Margin
-- ------------------------------------------------------------
SELECT
    ROUND(SUM(revenue), 2)                             AS total_revenue,
    ROUND(SUM(profit), 2)                               AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue),0), 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id)                              AS total_orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2)       AS avg_order_value
FROM stg_sales_orders;

-- ------------------------------------------------------------
-- 2. YoY and MoM Growth (CTE + window functions)
-- ------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue)                     AS revenue
    FROM stg_sales_orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month)                          AS prior_month_revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2)      AS mom_growth_pct,
    LAG(revenue, 12) OVER (ORDER BY month)                        AS revenue_year_ago,
    ROUND(100.0 * (revenue - LAG(revenue, 12) OVER (ORDER BY month))
        / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2)   AS yoy_growth_pct
FROM monthly_revenue
ORDER BY month;

-- ------------------------------------------------------------
-- 3. Region Performance Ranking
-- ------------------------------------------------------------
SELECT
    region,
    ROUND(SUM(revenue), 2)                                        AS revenue,
    ROUND(SUM(profit), 2)                                          AS profit,
    RANK() OVER (ORDER BY SUM(revenue) DESC)                        AS revenue_rank
FROM stg_sales_orders
GROUP BY region
ORDER BY revenue DESC;

-- ------------------------------------------------------------
-- 4. Category Performance
-- ------------------------------------------------------------
SELECT
    category,
    ROUND(SUM(revenue), 2)      AS revenue,
    ROUND(SUM(profit), 2)        AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue),0), 2) AS margin_pct
FROM stg_sales_orders
GROUP BY category
ORDER BY revenue DESC;

-- ------------------------------------------------------------
-- 5. Top 10 Products by Revenue (window function)
-- ------------------------------------------------------------
SELECT product_name, category, revenue, product_rank FROM (
    SELECT
        product_name,
        category,
        SUM(revenue) AS revenue,
        DENSE_RANK() OVER (ORDER BY SUM(revenue) DESC) AS product_rank
    FROM stg_sales_orders
    GROUP BY product_name, category
) ranked
WHERE product_rank <= 10;

-- ------------------------------------------------------------
-- 6. Top 10 Customers by Revenue
-- ------------------------------------------------------------
SELECT
    customer_id,
    region,
    customer_type,
    ROUND(SUM(revenue), 2) AS revenue,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS customer_rank
FROM stg_sales_orders
GROUP BY customer_id, region, customer_type
ORDER BY revenue DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 7. Average Order Value by Customer Type
-- ------------------------------------------------------------
SELECT
    customer_type,
    COUNT(DISTINCT order_id)                          AS orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2)    AS avg_order_value
FROM stg_sales_orders
GROUP BY customer_type
ORDER BY avg_order_value DESC;

-- ------------------------------------------------------------
-- 8. Inventory Turnover Proxy (units sold per product, as a
--    stand-in for turnover given no separate inventory table)
-- ------------------------------------------------------------
SELECT
    product_name,
    category,
    SUM(quantity)                                       AS units_sold,
    ROUND(SUM(quantity) * 1.0 / COUNT(DISTINCT DATE_TRUNC('month', order_date)), 2) AS avg_units_sold_per_month
FROM stg_sales_orders
GROUP BY product_name, category
ORDER BY units_sold DESC;

-- ------------------------------------------------------------
-- 9. View: Executive Sales Summary
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_executive_sales_summary AS
SELECT
    DATE_TRUNC('month', order_date)  AS month,
    region,
    category,
    customer_type,
    SUM(revenue)                      AS revenue,
    SUM(profit)                        AS profit,
    COUNT(DISTINCT order_id)            AS orders
FROM stg_sales_orders
GROUP BY DATE_TRUNC('month', order_date), region, category, customer_type;

-- ------------------------------------------------------------
-- 10. Stored function: revenue for a given region + date range
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_region_revenue(reg VARCHAR, start_date DATE, end_date DATE)
RETURNS NUMERIC AS $$
DECLARE result NUMERIC;
BEGIN
    SELECT ROUND(SUM(revenue), 2) INTO result
    FROM stg_sales_orders
    WHERE region = reg AND order_date BETWEEN start_date AND end_date;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
