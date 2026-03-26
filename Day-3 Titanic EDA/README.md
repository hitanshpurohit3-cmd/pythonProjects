# Titanic Survival Analysis (EDA with Pandas)

## Project Overview
This project performs **Exploratory Data Analysis (EDA)** on the Titanic dataset using **Pandas, NumPy, Matplotlib, and Seaborn**. The dataset is loaded directly from Seaborn, eliminating the need for a Kaggle account.

The goal is to analyze patterns and factors affecting passenger survival.

---

## Objectives
This project answers the following questions:

- What was the overall survival rate?
- How did survival vary by gender?
- How did passenger class affect survival?
- What is the age distribution of survivors vs non-survivors?
- Did embarkation port influence survival?

---

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

---

## Dataset
- Source: Seaborn built-in Titanic dataset
- Total Records: 891
- Total Features: 15

### Important Columns:
- `survived` — Survival (0 = No, 1 = Yes)
- `pclass` — Passenger Class (1st, 2nd, 3rd)
- `sex` — Gender
- `age` — Age
- `fare` — Ticket Fare
- `embarked` — Port of Embarkation

---

## 🔍 Exploratory Data Analysis

### 1. Overall Survival Rate
- Survival Rate ≈ **38.4%**
- Majority of passengers did not survive

**Visualizations:**
- Bar Chart (Survived vs Died)
- Pie Chart (Survival Proportion)

---

### 2. Survival by Gender
- Females had significantly higher survival rates than males

**Insight:**
- Reflects "Women and children first" evacuation strategy

**Visualizations:**
- Survival Rate Bar Chart
- Stacked Bar Chart

---

### 3. Survival by Passenger Class
- 1st Class → Highest survival
- 2nd Class → Moderate survival
- 3rd Class → Lowest survival

**Visualizations:**
- Bar Chart (Class vs Survival Rate)
- Heatmap (Class × Gender)

---

### 4. Age Distribution Analysis
- Compared age distributions of survivors and non-survivors

**Methods Used:**
- Histogram Overlay
- KDE Plot (Density Curve)

**Insight:**
- Younger passengers had slightly better survival chances

---

### 5. Embarkation Port Analysis

| Port Code | Location |
|----------|----------|
| S | Southampton, UK |
| C | Cherbourg, France |
| Q | Queenstown, Ireland |

**Findings:**
- Passenger distribution varies by port
- Survival rates differ slightly

**Visualization:**
- Horizontal Bar Chart

---

## 📈 Output Files

The following visualizations are saved:

- `titanic_01_overall.png`
- `titanic_02_gender.png`
- `titanic_03_class.png`
- `titanic_04_age.png`
- `titanic_05_ports.png`

---

## ⚙️ Installation & Usage

### Step 1: Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn