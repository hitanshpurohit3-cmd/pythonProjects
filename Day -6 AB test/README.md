# 📊 A/B Test Analyzer — Advanced Statistical Testing

## 📌 Project Overview

This project simulates and analyzes an A/B test comparing two variants (Control vs Treatment) using:

- Statistical hypothesis testing
- Confidence interval estimation
- Power analysis
- Data visualization dashboard
- Business recommendation report

The goal is to determine whether a new feature (treatment) significantly improves conversion rates.

---

## 🧠 Key Concepts Used

- Welch’s t-test  
- Proportion z-test  
- Confidence Intervals (95%)  
- Statistical Power & Sample Size  
- Bootstrap Simulation  
- Data Visualization (Matplotlib)  

---

## ⚙️ Tech Stack

- Python  
- NumPy  
- SciPy  
- Statsmodels  
- Matplotlib  

---

## 📁 Project Structure

```
A-B-Test-Analyzer/
│
├── ab_test.py
├── outputs/
│   ├── ab_conversion_chart.png
│   └── business_recommendation.txt
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ab-test-analyzer.git
cd ab-test-analyzer
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
python ab_test.py
```

---

## 📊 Output

### 1. Visualization Dashboard
Saved at:
```
outputs/ab_conversion_chart.png
```

Includes:
- Conversion rate comparison with confidence intervals  
- Bootstrap distribution of lift  
- Power analysis curve  
- Statistical summary table  

---

### 2. Business Recommendation Report
Saved at:
```
outputs/business_recommendation.txt
```

Includes:
- Executive summary  
- Statistical findings  
- Revenue impact estimation  
- Final recommendation (Ship / No Ship)  

---

## 📈 Sample Insights

- Treatment shows **~20% relative lift**  
- Statistically significant result (p < 0.05)  
- High statistical power (>80%)  
- Confidence interval excludes zero → strong evidence  

---

## 💼 Business Impact

Example (10,000 users/month):
- +200–250 additional conversions  
- ~$10,000+ monthly revenue uplift  
- ~$120,000+ annual impact  

---

## 🔍 Why This Project Matters

This project demonstrates:

✅ Real-world experimentation skills  
✅ Strong statistical foundation  
✅ Ability to translate data → business decisions  
✅ Production-level visualization and reporting  

---

## 🚧 Future Improvements

- Add real dataset support (CSV input)  
- Build Streamlit dashboard  
- Add segmentation analysis (device, region)  
- Automate experiment reporting pipeline  

---


## ⭐ If you found this useful

Give this repo a ⭐ and share it!