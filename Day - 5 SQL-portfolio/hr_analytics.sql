-- ============================================================
--  PROJECT 2: HR ANALYTICS DATABASE
--  Author   : HITANSH PUROHIT
--  Date     : 2026

--  WHAT THIS FILE COVERS
--  ─────────────────────
--  SECTION 0 : Schema design & table creation
--  SECTION 1 : Seed data
--  SECTION 2 : Exploratory queries
--  SECTION 3 : 6 Core HR analytics queries
--  SECTION 4 : Advanced queries (interview level)
--  SECTION 5 : Tomorrow's preview — indexes, views, EXPLAIN
-- ============================================================


-- ============================================================
-- SECTION 0: SCHEMA DESIGN
-- 4 tables — each owns one domain of HR data
-- Relationships: employees → departments (many-to-one)
--                salaries  → employees  (many-to-one, history)
--                reviews   → employees  (many-to-one, annual)
-- ============================================================

DROP TABLE IF EXISTS performance_reviews;
DROP TABLE IF EXISTS salaries;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- Departments: cost centres with budgets
CREATE TABLE departments (
    dept_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_name   TEXT    NOT NULL UNIQUE,
    budget      REAL    NOT NULL CHECK (budget > 0),
    location    TEXT    NOT NULL,
    created_at  TEXT    DEFAULT '2015-01-01'
);

-- Employees: core workforce table
CREATE TABLE employees (
    emp_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    gender      TEXT    NOT NULL CHECK (gender IN ('M','F','Other')),
    dept_id     INTEGER NOT NULL REFERENCES departments(dept_id),
    job_title   TEXT    NOT NULL,
    job_level   TEXT    NOT NULL
                CHECK (job_level IN ('Junior','Mid','Senior','Lead','Director','VP')),
    hire_date   TEXT    NOT NULL,
    manager_id  INTEGER REFERENCES employees(emp_id),   -- self-referencing
    is_active   INTEGER DEFAULT 1
);

-- Salaries: history of pay — one row per salary change
CREATE TABLE salaries (
    salary_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id         INTEGER NOT NULL REFERENCES employees(emp_id),
    amount         REAL    NOT NULL CHECK (amount > 0),
    effective_date TEXT    NOT NULL,
    reason         TEXT    -- 'hire','promotion','merit_raise','market_adj'
);

-- Performance Reviews: annual score + promotion decision
CREATE TABLE performance_reviews (
    review_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id       INTEGER NOT NULL REFERENCES employees(emp_id),
    review_year  INTEGER NOT NULL,
    score        INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
    -- 1=Needs Improvement 2=Below Avg 3=Meets 4=Exceeds 5=Outstanding
    promoted     INTEGER NOT NULL DEFAULT 0 CHECK (promoted IN (0,1)),
    reviewer_id  INTEGER REFERENCES employees(emp_id),
    notes        TEXT
);


-- ============================================================
-- SECTION 1: SEED DATA
-- ============================================================

INSERT INTO departments (dept_name, budget, location) VALUES
('Engineering', 850000, 'New York'),
('Marketing',   400000, 'Chicago'),
('Sales',       600000, 'Houston'),
('HR',          250000, 'Seattle'),
('Finance',     500000, 'Boston');

INSERT INTO employees (name, gender, dept_id, job_title, job_level, hire_date, manager_id) VALUES
('Alice Morgan', 'F', 1, 'Engineering Director', 'Director', '2016-03-01', NULL),
('Bob Chen',     'M', 1, 'Senior Engineer',      'Senior',   '2019-06-15', 1),
('Karen Lee',    'F', 1, 'Engineer',             'Mid',      '2020-07-07', 1),
('Leo Zhang',    'M', 1, 'Junior Engineer',      'Junior',   '2022-03-25', 2),
('Clara Davis',  'F', 2, 'Marketing Lead',       'Lead',     '2018-08-20', NULL),
('David Kim',    'M', 2, 'Marketing Analyst',    'Mid',      '2022-01-10', 5),
('Priya Patel',  'F', 2, 'Marketing Analyst',    'Mid',      '2021-05-18', 5),
('Eva Russo',    'F', 3, 'Sales VP',             'VP',       '2017-05-05', NULL),
('Frank Liu',    'M', 3, 'Senior Sales Rep',     'Senior',   '2020-11-30', 8),
('Mia Torres',   'F', 3, 'Sales Rep',            'Mid',      '2021-08-12', 8),
('Sam Okafor',   'M', 3, 'Junior Sales Rep',     'Junior',   '2023-02-01', 9),
('Grace Tan',    'F', 4, 'HR Director',          'Director', '2016-02-14', NULL),
('Henry Park',   'M', 4, 'HR Specialist',        'Mid',      '2023-01-20', 12),
('Isla Brown',   'F', 5, 'Finance Manager',      'Senior',   '2019-09-01', NULL),
('Jake Wilson',  'M', 5, 'Financial Analyst',    'Mid',      '2021-04-18', 14);

INSERT INTO salaries (emp_id, amount, effective_date, reason) VALUES
-- Current salaries (2023)
(1,  130000, '2023-01-01', 'merit_raise'),
(2,  110000, '2023-01-01', 'merit_raise'),
(3,   85000, '2023-01-01', 'merit_raise'),
(4,   72000, '2023-01-01', 'hire'),
(5,   95000, '2023-01-01', 'promotion'),
(6,   68000, '2023-01-01', 'merit_raise'),
(7,   71000, '2023-01-01', 'merit_raise'),
(8,  120000, '2023-01-01', 'merit_raise'),
(9,   78000, '2023-01-01', 'merit_raise'),
(10,  65000, '2023-01-01', 'hire'),
(11,  58000, '2023-01-01', 'hire'),
(12,  98000, '2023-01-01', 'merit_raise'),
(13,  58000, '2023-01-01', 'hire'),
(14, 115000, '2023-01-01', 'merit_raise'),
(15,  70000, '2023-01-01', 'merit_raise'),
-- Historical salaries (2021) — for tenure/growth analysis
(1,  118000, '2021-01-01', 'merit_raise'),
(2,   98000, '2021-01-01', 'hire'),
(5,   88000, '2021-01-01', 'hire'),
(8,  110000, '2021-01-01', 'merit_raise'),
(14, 105000, '2021-01-01', 'merit_raise');

INSERT INTO performance_reviews (emp_id, review_year, score, promoted, reviewer_id) VALUES
(1,  2022, 5, 0, NULL),
(2,  2022, 4, 1, 1),
(3,  2022, 3, 0, 1),
(4,  2022, 2, 0, 2),
(5,  2022, 5, 1, NULL),
(6,  2022, 3, 0, 5),
(7,  2022, 4, 0, 5),
(8,  2022, 5, 0, NULL),
(9,  2022, 4, 1, 8),
(10, 2022, 3, 0, 8),
(11, 2022, 2, 0, 9),
(12, 2022, 4, 0, NULL),
(13, 2022, 2, 0, 12),
(14, 2022, 5, 1, NULL),
(15, 2022, 4, 1, 14);


-- ============================================================
-- SECTION 2: EXPLORATORY QUERIES
-- ============================================================

-- Row counts
SELECT 'departments' AS tbl, COUNT(*) AS rows FROM departments UNION ALL
SELECT 'employees',          COUNT(*)          FROM employees   UNION ALL
SELECT 'salaries',           COUNT(*)          FROM salaries    UNION ALL
SELECT 'performance_reviews',COUNT(*)          FROM performance_reviews;

-- Headcount by department and gender
SELECT d.dept_name,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female,
       SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male,
       COUNT(*) AS total
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.is_active = 1
GROUP BY d.dept_name
ORDER BY total DESC;

-- Salary range overview
SELECT
    MIN(amount) AS min_salary,
    MAX(amount) AS max_salary,
    ROUND(AVG(amount),2) AS avg_salary,
    COUNT(*) AS total_salary_records
FROM salaries
WHERE effective_date >= '2023-01-01';


-- ============================================================
-- SECTION 3: CORE HR ANALYTICS QUERIES
-- ============================================================

-- ── QUERY 1: Gender Pay Gap Analysis ────────────────────────
-- Business question: "Is there a measurable pay disparity by gender?"
-- Concept used: CASE WHEN inside aggregate, division, subgroup stats
SELECT
    e.gender,
    COUNT(*)                         AS headcount,
    ROUND(MIN(s.amount),  2)         AS min_salary,
    ROUND(AVG(s.amount),  2)         AS avg_salary,
    ROUND(MAX(s.amount),  2)         AS max_salary,
    ROUND(
        -- median approximation using percentile_cont equivalent
        (MIN(s.amount) + MAX(s.amount)) / 2.0
    , 2)                             AS approx_median
FROM employees e
JOIN salaries s ON e.emp_id = s.emp_id
WHERE s.effective_date >= '2023-01-01'
GROUP BY e.gender;

-- Pay gap % (single number)
SELECT
    ROUND(AVG(CASE WHEN e.gender = 'M' THEN s.amount END), 2) AS avg_male_salary,
    ROUND(AVG(CASE WHEN e.gender = 'F' THEN s.amount END), 2) AS avg_female_salary,
    ROUND(
        100.0 * (
            AVG(CASE WHEN e.gender = 'M' THEN s.amount END) -
            AVG(CASE WHEN e.gender = 'F' THEN s.amount END)
        ) /
        NULLIF(AVG(CASE WHEN e.gender = 'F' THEN s.amount END), 0)
    , 2)                                                        AS pay_gap_pct
FROM employees e
JOIN salaries s ON e.emp_id = s.emp_id
WHERE s.effective_date >= '2023-01-01';


-- ── QUERY 2: Department Headcount vs Budget Utilization ─────
-- Business question: "Which departments are over or under budget?"
-- Concept used: LEFT JOIN + multiple aggregates + arithmetic
SELECT
    d.dept_name,
    d.location,
    d.budget,
    COUNT(e.emp_id)                            AS headcount,
    ROUND(SUM(s.amount), 2)                    AS total_salary_cost,
    ROUND(d.budget - SUM(s.amount), 2)         AS remaining_budget,
    ROUND(100.0 * SUM(s.amount) / d.budget, 1) AS budget_used_pct,
    CASE
        WHEN SUM(s.amount) > d.budget          THEN 'OVER BUDGET ⚠️'
        WHEN SUM(s.amount) > d.budget * 0.9   THEN 'Near Limit'
        ELSE                                        'Healthy'
    END                                        AS budget_status
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id AND e.is_active = 1
LEFT JOIN salaries  s ON e.emp_id  = s.emp_id  AND s.effective_date >= '2023-01-01'
GROUP BY d.dept_id, d.dept_name, d.location, d.budget
ORDER BY budget_used_pct DESC;


-- ── QUERY 3: Top Performers by Department ───────────────────
-- Business question: "Who are the high performers in each team?"
-- Concept used: CTE + RANK() OVER (PARTITION BY dept)
WITH ranked_performers AS (
    SELECT
        e.emp_id,
        e.name,
        e.job_title,
        e.job_level,
        d.dept_name,
        pr.score,
        s.amount                          AS current_salary,
        RANK() OVER (
            PARTITION BY e.dept_id
            ORDER BY pr.score DESC, s.amount DESC
        )                                 AS dept_rank
    FROM employees e
    JOIN departments d          ON e.dept_id = d.dept_id
    JOIN performance_reviews pr ON e.emp_id  = pr.emp_id
    JOIN salaries s             ON e.emp_id  = s.emp_id
    WHERE pr.review_year = 2022
      AND s.effective_date >= '2023-01-01'
      AND e.is_active = 1
)
SELECT dept_name, name, job_title, score, current_salary, dept_rank
FROM ranked_performers
WHERE dept_rank <= 2      -- top 2 per department
ORDER BY dept_name, dept_rank;


-- ── QUERY 4: Tenure Analysis using LAG ──────────────────────
-- Business question: "How are hires spaced within each department?"
-- Concept used: LAG() OVER (PARTITION BY ...) + julianday() for date diff
SELECT
    e.name,
    d.dept_name,
    e.job_level,
    e.hire_date,
    -- previous hire date within the same department
    LAG(e.hire_date) OVER (
        PARTITION BY e.dept_id
        ORDER BY e.hire_date
    )                                                    AS prev_hire_date,
    -- days between this hire and previous hire in same dept
    CAST(
        julianday(e.hire_date) -
        julianday(
            LAG(e.hire_date) OVER (PARTITION BY e.dept_id ORDER BY e.hire_date)
        )
    AS INTEGER)                                          AS days_between_hires,
    -- total tenure in years from today
    ROUND(
        (julianday('2024-01-01') - julianday(e.hire_date)) / 365.25
    , 1)                                                 AS tenure_years
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.is_active = 1
ORDER BY d.dept_name, e.hire_date;


-- ── QUERY 5: Salary Band Classification with CASE WHEN ──────
-- Business question: "How is pay distributed across seniority bands?"
-- Concept used: CASE WHEN for bucketing + GROUP BY + percentage
WITH banded AS (
    SELECT
        e.emp_id,
        e.name,
        e.job_level,
        s.amount,
        CASE
            WHEN s.amount <  65000                    THEN '1. Entry      (<$65K)'
            WHEN s.amount BETWEEN 65000  AND 85000    THEN '2. Mid        ($65K–$85K)'
            WHEN s.amount BETWEEN 85001  AND 110000   THEN '3. Senior     ($85K–$110K)'
            WHEN s.amount BETWEEN 110001 AND 130000   THEN '4. Lead/Mgr   ($110K–$130K)'
            ELSE                                           '5. Executive  (>$130K)'
        END AS salary_band
    FROM employees e
    JOIN salaries s ON e.emp_id = s.emp_id
    WHERE s.effective_date >= '2023-01-01'
      AND e.is_active = 1
)
SELECT
    salary_band,
    COUNT(*)                           AS headcount,
    ROUND(AVG(amount), 2)              AS avg_salary_in_band,
    ROUND(MIN(amount), 2)              AS band_min,
    ROUND(MAX(amount), 2)              AS band_max,
    ROUND(100.0 * COUNT(*) /
          SUM(COUNT(*)) OVER (), 1)    AS pct_of_workforce
FROM banded
GROUP BY salary_band
ORDER BY salary_band;


-- ── QUERY 6: Promotion Rate by Department ───────────────────
-- Business question: "Which departments invest most in promoting talent?"
-- Concept used: JOIN + SUM of boolean + percentage calculation
SELECT
    d.dept_name,
    COUNT(pr.emp_id)                                         AS total_reviewed,
    SUM(pr.promoted)                                         AS total_promoted,
    SUM(CASE WHEN pr.score = 5 THEN 1 ELSE 0 END)           AS outstanding_performers,
    ROUND(100.0 * SUM(pr.promoted) / COUNT(pr.emp_id), 1)   AS promotion_rate_pct,
    -- Of those promoted, what was their avg score?
    ROUND(AVG(CASE WHEN pr.promoted = 1 THEN pr.score END), 2) AS avg_score_of_promoted
FROM departments d
JOIN employees e           ON d.dept_id = e.dept_id
JOIN performance_reviews pr ON e.emp_id = pr.emp_id
WHERE pr.review_year = 2022
  AND e.is_active = 1
GROUP BY d.dept_name
ORDER BY promotion_rate_pct DESC;


-- ============================================================
-- SECTION 4: ADVANCED QUERIES 
-- ============================================================

-- ADVANCED 1: Salary Growth per Employee (2021 → 2023)
-- Compares oldest and newest salary record per person
WITH salary_history AS (
    SELECT
        emp_id,
        amount,
        effective_date,
        ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY effective_date ASC)  AS oldest,
        ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY effective_date DESC) AS newest
    FROM salaries
)
SELECT
    e.name,
    d.dept_name,
    old_s.amount                                          AS starting_salary,
    new_s.amount                                          AS current_salary,
    ROUND(new_s.amount - old_s.amount, 2)                 AS salary_growth,
    ROUND(100.0 * (new_s.amount - old_s.amount) /
          old_s.amount, 1)                                AS growth_pct
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
JOIN salary_history old_s ON e.emp_id = old_s.emp_id AND old_s.oldest = 1
JOIN salary_history new_s ON e.emp_id = new_s.emp_id AND new_s.newest = 1
WHERE old_s.effective_date != new_s.effective_date  -- only if salary changed
ORDER BY growth_pct DESC;


-- ADVANCED 2: Manager vs Direct Report Salary Comparison
-- Are managers always paid more than their reports?
SELECT
    mgr.name                AS manager,
    emp.name                AS direct_report,
    d.dept_name,
    mgr_sal.amount          AS manager_salary,
    emp_sal.amount          AS report_salary,
    ROUND(mgr_sal.amount - emp_sal.amount, 2) AS salary_difference,
    CASE
        WHEN mgr_sal.amount <= emp_sal.amount THEN 'Report earns MORE than manager!'
        ELSE 'Normal'
    END                     AS flag
FROM employees emp
JOIN employees mgr  ON emp.manager_id     = mgr.emp_id
JOIN departments d  ON emp.dept_id        = d.dept_id
JOIN salaries emp_sal ON emp.emp_id       = emp_sal.emp_id
                      AND emp_sal.effective_date >= '2023-01-01'
JOIN salaries mgr_sal ON mgr.emp_id       = mgr_sal.emp_id
                      AND mgr_sal.effective_date >= '2023-01-01'
ORDER BY salary_difference;


-- ADVANCED 3: High Performers Who Were NOT Promoted (Flight Risk)
-- Employees scoring 4-5 but not promoted — retention risk
SELECT
    e.name,
    d.dept_name,
    e.job_level,
    pr.score,
    s.amount AS current_salary,
    'Flight Risk — Review Compensation' AS recommendation
FROM employees e
JOIN departments d           ON e.dept_id = d.dept_id
JOIN performance_reviews pr  ON e.emp_id  = pr.emp_id
JOIN salaries s              ON e.emp_id  = s.emp_id
WHERE pr.review_year = 2022
  AND pr.score >= 4
  AND pr.promoted = 0
  AND s.effective_date >= '2023-01-01'
  AND e.is_active = 1
ORDER BY pr.score DESC, s.amount ASC;


-- ============================================================
-- SECTION 5: 
-- ============================================================

-- PREVIEW 1: CREATE VIEW — reusable saved query
CREATE VIEW IF NOT EXISTS vw_employee_summary AS
SELECT
    e.emp_id,
    e.name,
    e.gender,
    e.job_title,
    e.job_level,
    e.hire_date,
    d.dept_name,
    s.amount AS current_salary,
    pr.score AS latest_review_score,
    pr.promoted AS was_promoted_2022
FROM employees e
JOIN departments d          ON e.dept_id = d.dept_id
JOIN salaries s             ON e.emp_id  = s.emp_id
                           AND s.effective_date >= '2023-01-01'
LEFT JOIN performance_reviews pr ON e.emp_id = pr.emp_id
                                AND pr.review_year = 2022
WHERE e.is_active = 1;

-- Use the view like a table:
SELECT * FROM vw_employee_summary ORDER BY current_salary DESC;

-- PREVIEW 2: INDEXES for performance
CREATE INDEX IF NOT EXISTS idx_emp_dept       ON employees(dept_id);
CREATE INDEX IF NOT EXISTS idx_emp_manager    ON employees(manager_id);
CREATE INDEX IF NOT EXISTS idx_sal_emp        ON salaries(emp_id);
CREATE INDEX IF NOT EXISTS idx_sal_date       ON salaries(effective_date);
CREATE INDEX IF NOT EXISTS idx_review_emp     ON performance_reviews(emp_id);
CREATE INDEX IF NOT EXISTS idx_review_year    ON performance_reviews(review_year);

-- PREVIEW 3: EXPLAIN QUERY PLAN

EXPLAIN QUERY PLAN
SELECT e.name, s.amount, pr.score
FROM employees e
JOIN salaries s             ON e.emp_id = s.emp_id
JOIN performance_reviews pr ON e.emp_id = pr.emp_id
WHERE e.dept_id = 1
  AND s.effective_date >= '2023-01-01'
  AND pr.review_year = 2022;

-- ============================================================
-- END OF PROJECT 2
-- ============================================================
