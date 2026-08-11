-- ============================================================
-- Sales Performance Executive Dashboard
-- 01_schema.sql — Database schema (DDL)
-- ============================================================

DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id     VARCHAR(10) PRIMARY KEY,
    customer_name   VARCHAR(100),
    region          VARCHAR(20),
    customer_type   VARCHAR(20) CHECK (customer_type IN ('Retail','Wholesale','Online'))
);

CREATE TABLE products (
    product_id      VARCHAR(10) PRIMARY KEY,
    product_name    VARCHAR(100),
    category        VARCHAR(50),
    unit_cost       NUMERIC(10,2),
    unit_price      NUMERIC(10,2)
);

CREATE TABLE order_lines (
    order_id        VARCHAR(10) PRIMARY KEY,
    order_date      DATE NOT NULL,
    customer_id     VARCHAR(10) REFERENCES customers(customer_id),
    product_id      VARCHAR(10) REFERENCES products(product_id),
    quantity        INT NOT NULL,
    discount_pct    NUMERIC(4,2) DEFAULT 0,
    revenue         NUMERIC(12,2) NOT NULL,
    cost            NUMERIC(12,2) NOT NULL,
    profit          NUMERIC(12,2) NOT NULL
);

CREATE INDEX idx_orders_date ON order_lines(order_date);
CREATE INDEX idx_orders_customer ON order_lines(customer_id);
CREATE INDEX idx_orders_product ON order_lines(product_id);
