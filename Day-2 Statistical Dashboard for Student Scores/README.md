## Statistical Dashboard - Student Exam Scores

Analyzes a synthetic dataset of 200 student exam scores using pure Numpy.

**Techniques used:**
-Data generation with 'np.random.normal()` and boundary clipping
-Descriptive statistics: mean, median, std, percentiles
-Boolean masking for conditional counting (pass/distinction rates)
-Distribution visualisation with annoted histogram (Matplotlib)

**Key insight:** The passing rate and distinction rate are computed using Numpy boolean indexing - no loops, no pandas, 
just vectorized operations.

Run: `jupyter notebook student_scores.ipynb
