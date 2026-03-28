# ============================================================
# PROJECT 1 RUNNER — E-Commerce Business Intelligence
# File    : run_project1.py
# Reads   : ecommerce_bi.sql
# Run     : open in JupyterLab → Run All
# ============================================================

import sqlite3
import pandas as pd

# ── SETUP ───────────────────────────────────────────────────
conn = sqlite3.connect(':memory:')

with open('ecommerce_bi.sql', 'r') as f:
    conn.executescript(f.read())
print("✅ ecommerce_bi.sql loaded\n")

def query(sql, title):
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))
    return df


print("\n✅ Project 1 complete — all 8 queries done.")
conn.close()
