## Linear Regression from Scratch — NumPy Only

Built a complete gradient descent optimizer without any ML libraries.

**What's implemented:**
- Synthetic dataset generation with controlled noise
- MSE loss function computed with NumPy vectorized ops
- Manual gradient calculation (dL/dm, dL/db) via chain rule
- Parameter updates over 1000 epochs
- Convergence visualization (loss curve + fitted line)

**Result:** Recovered slope ≈ 3.0 and intercept ≈ 7.0 from noisy data

**Skills demonstrated:** ML math fundamentals, gradient descent,
NumPy vectorization, loss optimization without ML frameworks

**Run:** `python linear_regression.ipynb
