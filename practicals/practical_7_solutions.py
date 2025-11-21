import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from functions import bernoulli_sim

# 2.1

n = 100

# grid of p values between 0 and 1
p = np.linspace(0, 1, 500)

# MSE formulas
MSE_p1 = (p * (1 - p)) / n
MSE_p2 = (n * p * (1 - p)) / (n + 2) ** 2 + ((1 - 2 * p) / (n + 2)) ** 2

# plot
plt.figure(figsize=(8, 6))
plt.plot(p, MSE_p1, "r-", label=r"$MSE(\hat{p}_1, p)$")
plt.plot(p, MSE_p2, "b-", label=r"$MSE(\hat{p}_2, p)$")
plt.xlabel("p")
plt.ylabel("MSE")
plt.title(f"Comparison of MSE for n = {n}")
plt.legend()
plt.grid(True)
plt.show()

# 2.2

# 2.2.1
# Parameters
n = 100
p = 0.1
nsim = 500

# Run simulation
df = bernoulli_sim(n, p, nsim)

# Boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([df["hatp1"], df["hatp2"]], labels=[r"$\hat{p}_1$", r"$\hat{p}_2$"])
plt.axhline(y=p, color="red", linestyle="--", label="True p")
plt.title(f"Distribution of estimators (n={n}, p={p}, nsim={nsim})")
plt.ylabel("Estimator value")
plt.legend()
plt.show()

# 2.2.2

# Parameters
p = 0.1
nsim = 500
n_values = [50, 100, 500, 1000, 10000]

# Collect results
results_p1 = []
results_p2 = []
for n in n_values:
    result = bernoulli_sim(n, p, nsim)
    results_p1.append(result["hatp1"])
    results_p2.append(result["hatp2"])

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Plot for hatp1
axes[0].boxplot(results_p1, labels=n_values)
axes[0].axhline(y=p, color="red", linestyle="--", label="True p")
axes[0].set_title(r"Behavior of $\hat{p}_1$")
axes[0].set_xlabel("Sample size n")
axes[0].set_ylabel("Estimator value")
axes[0].legend()
axes[0].grid(True, linestyle=":")

# Plot for hatp2
axes[1].boxplot(results_p2, labels=n_values)
axes[1].axhline(y=p, color="red", linestyle="--", label="True p")
axes[1].set_title(r"Behavior of $\hat{p}_2$")
axes[1].set_xlabel("Sample size n")
axes[1].legend()
axes[1].grid(True, linestyle=":")

plt.suptitle(f"Comparison of Estimators (p={p}, nsim={nsim})", fontsize=14)
plt.tight_layout()
plt.show()
