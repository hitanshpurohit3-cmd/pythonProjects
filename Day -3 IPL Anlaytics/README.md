# 🏏 IPL Data Analysis (EDA with Pandas)

## 📌 Project Overview
This project performs **Exploratory Data Analysis (EDA)** on the Indian Premier League (IPL) dataset using **Pandas, NumPy, Matplotlib, and Seaborn**.

The goal is to analyze patterns in player performance, bowling efficiency, match outcomes, and partnerships.

---

## 🎯 Objectives
This project answers the following questions:

- Who are the top run scorers in IPL history?
- Which bowlers have the best economy rates?
- Does winning the toss impact match results?
- What are the highest partnerships in IPL?
- Who has won the most Player of the Match awards?

---

## 🛠️ Tech Stack
- Python  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  

---

## Dataset
**Source:** Kaggle IPL Dataset  

**Files Used:**
- `deliveries.csv` — Ball-by-ball data (~179K rows)
- `matches.csv` — Match-level data (~756 rows)

### Important Columns:

**Deliveries Dataset:**
- `batsman` — Player scoring runs  
- `bowler` — Bowler name  
- `batsman_runs` — Runs scored  
- `total_runs` — Total runs in a delivery  
- `player_dismissed` — Wicket info  

**Matches Dataset:**
- `season` — IPL season  
- `city` — Match location  
- `winner` — Match winner  
- `toss_winner` — Toss winner  
- `toss_decision` — Bat or field  
- `player_of_match` — Best performer  

---

## 🔍 Exploratory Data Analysis

### 1. Top Run Scorers
- Identified top 10 batsmen based on total runs
- Calculated:
  - Total runs  
  - Number of innings  
  - Average runs per innings  

**Visualization:**
- Horizontal bar chart of top scorers  

---

### 2. Best Bowling Economy
- Formula used:

  Economy Rate = (Runs Conceded / Balls Bowled) × 6  

- Applied filter:
  - Minimum 20 overs bowled  

**Insight:**
- Economy below 7 is considered excellent  

**Visualization:**
- Bar chart with benchmark line  

---

### 3. Toss Impact on Match Outcome
- Created feature:

  toss_win_match_win = toss_winner == winner  

**Analysis:**
- Win rate after choosing to bat vs field  
- Team-wise toss advantage  

---

### 4. Highest Partnerships
- Calculated runs scored by batting pairs  
- Standardized pair names (A-B = B-A)  

**Insight:**
- Strong partnerships significantly influence match outcomes  

---

### 5. Player of the Match Analysis
- Counted total awards per player  

**Insight:**
- Highlights most impactful players in IPL history  

---

## ⚙️ Installation & Usage

### Step 1: Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn