# 🏠 House Price Feature Correlation Analysis for ML

A comprehensive feature correlation analysis project designed to identify key variables for machine learning models predicting house prices.

This project generates **3 analytical visualizations** to understand relationships, distributions, and feature importance.

---

## 🚀 Project Highlights

- 📊 Correlation heatmap for feature relationships
- 🔗 Pairplot for top predictive features
- 📉 Distribution + boxplot analysis for skewness detection
- 🎯 Synthetic dataset modeled on Kaggle House Prices dataset
- 🧠 ML-focused insights for feature selection and preprocessing

---

## 🖼️ Visual Outputs

### 🔥 Correlation Heatmap
![Heatmap](outputs/project2a_heatmap.png)

### 🔗 Pairplot (Top Features)
![Pairplot](outputs/project2b_pairplot.png)

### 📉 Distribution Analysis
![Distributions](outputs/project2c_distributions.png)

---

## 🧠 Key Insights

- **Top Predictors:**
  OverallQual, GrLivArea, and TotalBsmtSF strongly influence SalePrice

- **Skewness Problem:**
  SalePrice, LotArea, and GrLivArea are right-skewed → require log transformation

- **Multicollinearity Alert:**
  GrLivArea and TotalBsmtSF are highly correlated → may affect linear models

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib

---

## 📂 Project Structure

house-price-correlation-analysis/
│── analysis.py
│── README.md
│── requirements.txt
│── outputs/
│     ├── project2a_heatmap.png
│     ├── project2b_pairplot.png
│     └── project2c_distributions.png

---

## ⚙️ Installation & Setup

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

---

## ▶️ Run the Project

python analysis.py

Outputs saved in:
outputs/

---

## 📌 Data Note

- Synthetic dataset inspired by Kaggle House Prices
- Suitable for ML feature selection and preprocessing

---

## 💡 Future Improvements

- Apply regression models
- Feature engineering pipeline
- Deploy as web dashboard

---
