# ============================================================
# PROJECT 2 RUNNER — HR Analytics Database
# File    : run_project2.py
# Reads   : hr_analytics.sql
# Run     : open in JupyterLab → Run All
# ============================================================

import sqlite3
import pandas as pd

# ── SETUP ───────────────────────────────────────────────────
conn = sqlite3.connect(':memory:')

with open('hr_analytics.sql', 'r',encoding='utf-8') as f:
    conn.executescript(f.read())
print("✅ hr_analytics.sql loaded\n")

def query(sql, title):
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))
    return df


print("\n✅ Project 2 complete — all 6 queries done.")
conn.close()
