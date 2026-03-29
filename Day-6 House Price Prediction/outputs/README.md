# 🏠 House Price Prediction — End-to-End Regression Pipeline

🚀 **Resume Highlight**  
Built an end-to-end regression pipeline with feature engineering and polynomial modeling — improved R² performance using advanced techniques.

---

## 📌 Project Overview

This project predicts house prices using the California Housing dataset with a complete machine learning pipeline:

- Data exploration & visualization
- Feature engineering
- Multiple regression models
- Model evaluation & comparison
- Performance visualization dashboard

The goal is to improve prediction accuracy using engineered and polynomial features.

---

## 🧠 Key Concepts Used

- Linear Regression  
- Ridge Regression (Regularization)  
- Polynomial Feature Engineering  
- Feature Scaling (StandardScaler)  
- Cross Validation (5-Fold)  
- Model Evaluation (MAE, RMSE, R²)  
- Residual Analysis  
- Permutation Feature Importance  

---

## ⚙️ Tech Stack

- Python  
- NumPy  
- Pandas  
- Scikit-learn  
- Matplotlib  
- Seaborn  

---

## 📁 Project Structure

```
House-Price-Prediction/
│
├── house_price.py
├── outputs/
│   ├── correlation_heatmap.png
│   └── actual_vs_predicted.png
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/house-price-prediction.git
cd house-price-prediction
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the project
```bash
python house_price.py
```

---

## 📊 Dataset

- Source: Scikit-learn built-in dataset  
- Name: California Housing Dataset  
- Target: `MedHouseValue` (median house value in 100k USD)  

### Features include:
- Median Income  
- House Age  
- Average Rooms  
- Population  
- Latitude / Longitude  

---

## 🔍 Feature Engineering

Custom features created to improve model performance:

- Rooms per person  
- Bedrooms per room  
- Population density  
- Income per room  
- Log-transformed population  
- Squared income feature  

---

## 🤖 Models Used

1. **Baseline Linear Regression**
2. **Linear Regression + Engineered Features**
3. **Polynomial Regression (Degree 2) + Ridge Regularization**

---

## 📈 Model Evaluation Metrics

- MAE (Mean Absolute Error)  
- RMSE (Root Mean Squared Error)  
- R² Score (Model Accuracy)  

---

## 📊 Output

### 1. Correlation Heatmap
Saved at:
```
outputs/correlation_heatmap.png
```

Shows relationships between all features and target variable.

---

### 2. Model Evaluation Dashboard
Saved at:
```
outputs/actual_vs_predicted.png
```

Includes:
- Actual vs Predicted (Baseline vs Polynomial)  
- Residual plot  
- Model comparison (R²)  
- MAE vs RMSE comparison  
- Residual distribution  

---

## 📉 Key Insights

- Feature engineering improves baseline model performance  
- Polynomial features capture non-linear relationships  
- Ridge regression prevents overfitting  
- Residuals approximately follow normal distribution → good model fit  

---

## 📊 Performance Improvement

- Baseline model provides solid benchmark  
- Polynomial model improves R² significantly  
- Cross-validation ensures model stability  

---

## 💼 Business Impact

- Better pricing predictions → improved real estate decisions  
- Helps identify undervalued / overvalued properties  
- Useful for:
  - Real estate platforms  
  - Investment analysis  
  - Property valuation systems  

---

## 🔍 Why This Project Matters

This project demonstrates:

✅ End-to-end ML pipeline skills  
✅ Strong feature engineering capability  
✅ Model comparison & evaluation expertise  
✅ Real-world regression problem solving  
✅ Visualization & storytelling with data  

---

## 🚧 Future Improvements

- Add advanced models (XGBoost, Random Forest)  
- Hyperparameter tuning (GridSearchCV)  
- Deploy as a web app (Streamlit)  
- Add geographic visualizations (maps)  
- Use real-world housing datasets  

---

## ⭐ If you found this useful

Give this repo a ⭐ and share it!