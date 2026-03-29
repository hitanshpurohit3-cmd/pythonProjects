# 📊 Customer Churn Classifier — Logistic Regression

## 🚀 Project Overview
This project builds an **end-to-end machine learning pipeline** to predict customer churn using logistic regression. It analyzes customer behavior and identifies key factors driving churn, enabling businesses to take proactive retention actions.

---

## 🎯 Objective
- Predict whether a customer will churn (Yes/No)
- Achieve **80%+ accuracy**
- Identify **top churn drivers** for business insights

---

## 📂 Dataset
- **Telco Customer Churn Dataset**
- Source: Kaggle  
- Contains customer demographics, services, billing, and churn labels

---

## ⚙️ Tech Stack
- **Python**
- **NumPy, Pandas**
- **Matplotlib, Seaborn**
- **Scikit-learn**

---

## 🔄 Workflow Pipeline

### 1. Data Loading
- Loads dataset from CSV
- If missing → generates synthetic dataset with similar structure

### 2. Data Cleaning
- Removes unnecessary columns (`customerID`)
- Converts `TotalCharges` to numeric
- Handles missing values using median imputation

### 3. Feature Engineering
- Label encoding for binary features
- One-hot encoding for categorical variables
- Target variable conversion (Yes → 1, No → 0)

### 4. Train-Test Split
- 80/20 split using **stratification**
- Maintains churn class distribution

### 5. Model Training
- Pipeline:
  - StandardScaler
  - LogisticRegression
- Handles imbalance using `class_weight="balanced"`

---

## 📈 Model Performance

| Metric        | Description |
|--------------|------------|
| Accuracy     | Overall correctness |
| Precision    | Correct churn predictions |
| Recall       | Ability to detect churn |
| F1 Score     | Balance of precision & recall |
| ROC-AUC      | Model discrimination ability |

✔ Includes:
- Confusion Matrix  
- ROC Curve  
- Precision-Recall Tradeoff  
- Cross-validation (5-Fold)

---

## 🔍 Key Insights

### 🔺 Top Churn Drivers (Increase Risk)
- Month-to-month contracts
- Fiber optic internet
- Electronic check payments
- High monthly charges
- Low tenure

### 🔻 Churn Protectors (Reduce Risk)
- Long-term contracts (1–2 years)
- Tech support availability
- Online backup services
- Higher tenure
- Stable billing methods

---

## 📊 Visual Outputs
Saved in `/outputs` folder:

- `roc_curve.png` → Full evaluation dashboard  
- `top_churn_drivers.png` → Feature importance visualization  
- `classification_report.txt` → Detailed metrics report  

---

## 🧠 Business Impact
This model helps businesses:
- Identify **high-risk customers**
- Design **targeted retention strategies**
- Optimize **pricing & contract policies**
- Improve **customer lifetime value (CLV)**

---

## ▶️ How to Run

```bash
# 1. Create virtual environment
python -m venv churn_env

# 2. Activate environment
# Windows
churn_env\Scripts\activate

# Mac/Linux
source churn_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script
python churn_model.py
```

---

## 📌 Resume Highlight
**"Built a customer churn prediction model using logistic regression achieving 80%+ accuracy and identified top 5 churn drivers for actionable business insights."**

---

## 📁 Project Structure
```
project/
│
├── churn_model.py
├── requirements.txt
└── outputs/
    ├── roc_curve.png
    ├── top_churn_drivers.png
    └── classification_report.txt
```

---

## 🔮 Future Improvements
- Try advanced models (XGBoost, Random Forest)
- Hyperparameter tuning (GridSearchCV)
- Feature selection techniques
- Deploy as a web app (Streamlit / Flask)

---

## ✅ Status
✔ Completed  
✔ Production-ready pipeline    

---