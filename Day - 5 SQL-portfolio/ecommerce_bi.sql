-- ============================================================
--  PROJECT 1: E-COMMERCE BUSINESS INTELLIGENCE
--  Author   : HITANSH PUROHIT
--  Date     : 2026

--  WHAT THIS FILE COVERS
--  ─────────────────────
--  SECTION 0 : Database design & schema creation
--  SECTION 1 : Seed data (realistic sample data)
--  SECTION 2 : Exploratory / sanity-check queries
--  SECTION 3 : 8 Business Intelligence queries (KPIs)
--  SECTION 4 : Advanced — CTEs, Window Functions, Subqueries
--  SECTION 5 : Tomorrow's preview — indexes, EXPLAIN, views
-- ============================================================


-- ============================================================
-- SECTION 0: SCHEMA DESIGN
-- Why 4 tables? Normalization — avoid repeating customer data
-- on every order row. Each table has ONE responsibility.
-- ============================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customers: who buys from us
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    city          TEXT,
    country       TEXT    DEFAULT 'USA',
    signup_date   TEXT    NOT NULL,   -- format: YYYY-MM-DD
    is_active     INTEGER DEFAULT 1   -- 1=active, 0=churned
);

-- Products: what we sell
CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    price         REAL    NOT NULL CHECK (price > 0),
    stock_qty     INTEGER DEFAULT 0,
    is_listed     INTEGER DEFAULT 1   -- 1=live, 0=delisted
);

-- Orders: one row per transaction
CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date    TEXT    NOT NULL,
    status        TEXT    NOT NULL
                  CHECK (status IN ('completed','returned','pending','cancelled')),
    shipping_city TEXT
);

-- Order Items: line items inside each order (many-to-many bridge)
-- One order can have many products; one product can be in many orders
CREATE TABLE order_items (
    item_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL    NOT NULL CHECK (unit_price > 0)
    -- unit_price stored here (not from products) because prices change over time
);


-- ============================================================
-- SECTION 1: SEED DATA
-- ============================================================

INSERT INTO customers (name, email, city, signup_date, is_active) VALUES
('Alice Morgan',  'alice@mail.com',  'New York',    '2022-01-15', 1),
('Bob Chen',      'bob@mail.com',    'Chicago',     '2022-03-22', 1),
('Clara Davis',   'clara@mail.com',  'Houston',     '2022-05-10', 1),
('David Kim',     'david@mail.com',  'Seattle',     '2022-07-04', 1),
('Eva Russo',     'eva@mail.com',    'Boston',      '2022-09-18', 1),
('Frank Liu',     'frank@mail.com',  'Austin',      '2023-01-02', 1),
('Grace Tan',     'grace@mail.com',  'Denver',      '2023-03-14', 1),
('Henry Park',    'henry@mail.com',  'Miami',       '2023-06-28', 1),
('Isla Brown',    'isla@mail.com',   'Phoenix',     '2023-08-05', 1),
('Jake Wilson',   'jake@mail.com',   'Los Angeles', '2023-11-20', 0);  -- churned

INSERT INTO products (name, category, price, stock_qty, is_listed) VALUES
('Wireless Mouse',       'Electronics',  29.99,  150, 1),
('Mechanical Keyboard',  'Electronics',  89.99,   80, 1),
('USB-C Hub',            'Electronics',  49.99,  200, 1),
('Desk Lamp',            'Home Office',  34.99,  120, 1),
('Notebook Set',         'Stationery',   14.99,  300, 1),
('Standing Desk',        'Furniture',   349.99,   30, 1),
('Monitor Stand',        'Furniture',    59.99,   90, 1),
('Cable Organizer',      'Accessories',  12.99,  400, 1),
('Webcam HD',            'Electronics',  79.99,   60, 1),
('Blue-Light Glasses',   'Accessories',  24.99,  180, 1),
('Whiteboard Markers',   'Stationery',    8.99,  500, 1),
('Ergonomic Chair',      'Furniture',   499.99,   20, 1),
('Laptop Stand',         'Electronics',  39.99,  110, 1),
('Desk Pad',             'Accessories',  19.99,  250, 0); -- delisted, never ordered

INSERT INTO orders (customer_id, order_date, status, shipping_city) VALUES
(1,  '2023-01-10', 'completed', 'New York'),
(1,  '2023-03-22', 'completed', 'New York'),
(2,  '2023-02-14', 'completed', 'Chicago'),
(3,  '2023-04-01', 'completed', 'Houston'),
(3,  '2023-06-15', 'completed', 'Houston'),
(4,  '2023-05-20', 'returned',  'Seattle'),
(5,  '2023-07-08', 'completed', 'Boston'),
(5,  '2023-08-30', 'completed', 'Boston'),
(6,  '2023-09-12', 'completed', 'Austin'),
(7,  '2023-10-05', 'completed', 'Denver'),
(8,  '2023-11-18', 'completed', 'Miami'),
(9,  '2023-12-01', 'completed', 'Phoenix'),
(1,  '2023-12-20', 'completed', 'New York'),
(2,  '2023-11-05', 'completed', 'Chicago'),
(10, '2023-06-25', 'pending',   'Los Angeles');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1,  1,  2, 29.99), (1,  2,  1, 89.99),
(2,  6,  1,349.99),
(3,  3,  1, 49.99), (3,  9,  1, 79.99),
(4,  4,  2, 34.99),
(5,  5,  3, 14.99), (5,  7,  1, 59.99),
(6,  12, 1,499.99),
(7,  8,  4, 12.99), (7,  10, 1, 24.99),
(8,  2,  1, 89.99),
(9,  1,  1, 29.99),
(10, 3,  2, 49.99),
(11, 9,  1, 79.99),
(12, 6,  1,349.99),
(13, 11, 5,  8.99),
(14, 4,  1, 34.99), (14, 5,  2, 14.99),
(15, 7,  1, 59.99);


-- ============================================================
-- SECTION 2: EXPLORATORY QUERIES
-- Always run these first to understand your data
-- ============================================================

-- How many rows in each table?
SELECT 'customers'  AS tbl, COUNT(*) AS rows FROM customers  UNION ALL
SELECT 'products'   AS tbl, COUNT(*) AS rows FROM products   UNION ALL
SELECT 'orders'     AS tbl, COUNT(*) AS rows FROM orders     UNION ALL
SELECT 'order_items'AS tbl, COUNT(*) AS rows FROM order_items;

-- Order status breakdown
SELECT status, COUNT(*) AS count
FROM orders
GROUP BY status;

-- Price range per category
SELECT category,
       COUNT(*)         AS product_count,
       ROUND(MIN(price),2) AS cheapest,
       ROUND(MAX(price),2) AS most_expensive,
       ROUND(AVG(price),2) AS avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;


-- ============================================================
-- SECTION 3: BUSINESS INTELLIGENCE QUERIES
-- ============================================================

-- ── QUERY 1: Monthly Revenue Trend ──────────────────────────
-- Business question: "How is our revenue trending month over month?"
-- Concept used: JOIN + GROUP BY + string date function
SELECT
    strftime('%Y-%m', o.order_date)              AS month,
    COUNT(DISTINCT o.order_id)                   AS total_orders,
    SUM(oi.quantity)                             AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)   AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;


-- ── QUERY 2: Top 10 Customers by Lifetime Value (LTV) ───────
-- Business question: "Who are our most valuable customers ever?"
-- Concept used: multi-table JOIN + aggregate + ORDER + LIMIT
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.signup_date,
    COUNT(DISTINCT o.order_id)                   AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)   AS lifetime_value,
    ROUND(AVG(oi.quantity * oi.unit_price), 2)   AS avg_item_value
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name, c.city, c.signup_date
ORDER BY lifetime_value DESC
LIMIT 10;


-- ── QUERY 3: Product Category Performance ───────────────────
-- Business question: "Which categories drive the most revenue?"
-- Concept used: 3-table JOIN + GROUP BY + ORDER BY
SELECT
    p.category,
    COUNT(DISTINCT p.product_id)                 AS products_in_category,
    SUM(oi.quantity)                             AS total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)   AS category_revenue,
    ROUND(AVG(oi.unit_price), 2)                 AS avg_selling_price,
    -- revenue share across all categories
    ROUND(100.0 * SUM(oi.quantity * oi.unit_price) /
          SUM(SUM(oi.quantity * oi.unit_price)) OVER (), 1) AS revenue_pct
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o       ON oi.order_id  = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY category_revenue DESC;


-- ── QUERY 4: Customer Retention (Repeat Buyers) ─────────────
-- Business question: "What % of customers ordered more than once?"
-- Concept used: nested subquery + CASE WHEN + division
SELECT
    total_customers,
    repeat_customers,
    one_time_customers,
    ROUND(100.0 * repeat_customers   / total_customers, 1) AS retention_pct,
    ROUND(100.0 * one_time_customers / total_customers, 1) AS churn_pct
FROM (
    SELECT
        COUNT(DISTINCT customer_id)                               AS total_customers,
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)         AS repeat_customers,
        SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END)         AS one_time_customers
    FROM (
        SELECT customer_id, COUNT(order_id) AS order_count
        FROM orders
        WHERE status = 'completed'
        GROUP BY customer_id
    )
);


-- ── QUERY 5: Average Order Value (AOV) by Month ─────────────
-- Business question: "Is our average basket size growing?"
-- Concept used: JOIN + GROUP BY + division
SELECT
    strftime('%Y-%m', o.order_date)                          AS month,
    COUNT(DISTINCT o.order_id)                               AS order_count,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)               AS total_revenue,
    ROUND(SUM(oi.quantity * oi.unit_price) /
          COUNT(DISTINCT o.order_id), 2)                     AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;


-- ── QUERY 6: Products Never Ordered ─────────────────────────
-- Business question: "Which products have zero sales? Dead inventory?"
-- Concept used: LEFT JOIN + NULL check (classic "anti-join" pattern)
SELECT
    p.product_id,
    p.name,
    p.category,
    p.price,
    p.stock_qty,
    CASE WHEN p.is_listed = 1 THEN 'Live' ELSE 'Delisted' END AS listing_status
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL   -- NULL = no order row matched = never ordered
ORDER BY p.category;


-- ── QUERY 7: Running Total Revenue (Window Function) ────────
-- Business question: "What is our cumulative revenue over time?"
-- Concept used: CTE + SUM() OVER (window function)
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', o.order_date)               AS month,
        ROUND(SUM(oi.quantity * oi.unit_price), 2)    AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY month
)
SELECT
    month,
    monthly_revenue,
    -- SUM() OVER with ROWS frame = running total
    ROUND(SUM(monthly_revenue) OVER (
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2)  AS running_total,
    -- Month-over-month growth
    ROUND(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month), 2) AS mom_change
FROM monthly_revenue;


-- ── QUERY 8: Rank Customers by Spend per Category ───────────
-- Business question: "Who are the top spenders in each category?"
-- Concept used: CTE + RANK() OVER (PARTITION BY ...)
WITH category_spend AS (
    SELECT
        c.customer_id,
        c.name                                          AS customer,
        p.category,
        ROUND(SUM(oi.quantity * oi.unit_price), 2)     AS total_spend
    FROM customers c
    JOIN orders o       ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id    = oi.order_id
    JOIN products p     ON oi.product_id = p.product_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.name, p.category
)
SELECT
    category,
    customer,
    total_spend,
    -- RANK: gives same rank to ties, then skips (1,1,3)
    RANK()       OVER (PARTITION BY category ORDER BY total_spend DESC) AS rank_with_gaps,
    -- DENSE_RANK: gives same rank to ties, no skipping (1,1,2)
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_spend DESC) AS dense_rank,
    -- ROW_NUMBER: unique rank even for ties (1,2,3)
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_spend DESC) AS row_num
FROM category_spend
ORDER BY category, rank_with_gaps;


-- ============================================================
-- SECTION 4: ADVANCED QUERIES 
-- ============================================================

-- ADVANCED 1: Month-over-Month Revenue Growth %
WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.order_date)             AS month,
        ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month)  AS prev_month_revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) /
          NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly;


-- ADVANCED 2: Customer Segmentation (RFM-style)
-- Recency: when did they last order?
-- Frequency: how many orders?
-- Monetary: how much spent?
SELECT
    c.name,
    MAX(o.order_date)                                AS last_order_date,
    COUNT(DISTINCT o.order_id)                       AS order_frequency,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)       AS total_spent,
    CASE
        WHEN COUNT(DISTINCT o.order_id) >= 3
             AND SUM(oi.quantity * oi.unit_price) > 300  THEN 'Champion'
        WHEN COUNT(DISTINCT o.order_id) >= 2             THEN 'Loyal'
        WHEN MAX(o.order_date) >= '2023-10-01'           THEN 'Recent'
        ELSE 'At Risk'
    END AS customer_segment
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;


-- ADVANCED 3: Basket Analysis — What products are bought together?
-- Which product pairs appear in the same order most often?
SELECT
    p1.name  AS product_1,
    p2.name  AS product_2,
    COUNT(*) AS times_bought_together
FROM order_items a
JOIN order_items b  ON a.order_id   = b.order_id
                   AND a.product_id < b.product_id   -- avoid duplicates
JOIN products p1    ON a.product_id = p1.product_id
JOIN products p2    ON b.product_id = p2.product_id
GROUP BY p1.name, p2.name
ORDER BY times_bought_together DESC
LIMIT 10;


-- ============================================================
-- SECTION 5: 
-- Indexes, Views, EXPLAIN, Stored Procedures
-- ============================================================

-- PREVIEW 1: CREATE VIEW
-- A view is a saved query you can SELECT from like a table.
-- Tomorrow we'll use this in PostgreSQL with more advanced features.
CREATE VIEW IF NOT EXISTS vw_monthly_revenue AS
SELECT
    strftime('%Y-%m', o.order_date)             AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS revenue,
    COUNT(DISTINCT o.order_id)                  AS orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY month;

-- Query the view just like a table:
SELECT * FROM vw_monthly_revenue ORDER BY month;


-- PREVIEW 2: INDEXES
-- Indexes speed up queries on large datasets.
-- Tomorrow we'll measure the difference with EXPLAIN ANALYZE in PostgreSQL.
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date     ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_items_order     ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_items_product   ON order_items(product_id);

-- PREVIEW 3: EXPLAIN (SQLite version — tomorrow's PostgreSQL EXPLAIN ANALYZE is richer)
-- Shows the query plan: how SQLite decides to execute your query
EXPLAIN QUERY PLAN
SELECT c.name, SUM(oi.quantity * oi.unit_price) AS ltv
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id;

-- ============================================================
-- END OF PROJECT 1
-- ============================================================
