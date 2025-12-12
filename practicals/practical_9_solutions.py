import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, poisson
import numpy as np

#
# Theoretical exercises
#

# Exercise 1
# a.
1 - binom.cdf(k=524, n=1000, p=0.5)

# b.
binom.cdf(k=524, n=1000, p=0.55)

# Exercise 3
1 - binom.cdf(k=283, n=512, p=0.5)


#
# Practical exercises
#

# 1.a
x = np.arange(0, 21)
fig = plt.figure(figsize=(6, 4))
plt.bar(x, poisson.pmf(x, mu=8), width=0.8, alpha=0.6, label=r"Poisson($\lambda$=8)")
plt.plot(
    x,
    norm.pdf(x, loc=8, scale=np.sqrt(8)),
    "r-",
    label="Normal($\mu$=8, $\sigma^2=8$)",
)
plt.xlabel("x")
plt.ylabel("Probability / Density")
plt.legend()
plt.title("Poisson vs Normal Approximation")
plt.show()

# 1.b
fig = plt.figure(figsize=(6, 4))
plt.plot(x, poisson.cdf(x, mu=8), "bo-", label="Poisson CDF")
plt.plot(x, norm.cdf(x, loc=8, scale=np.sqrt(8)), "r--", label="Normal CDF")
plt.xlabel("x")
plt.ylabel("Cumulative Probability")
plt.legend()
plt.title("CDF Comparison: Poisson vs Normal")
plt.show()

# 1.c
n = 100
p = (np.arange(1, n + 1) - 0.5) / n
q_pois = poisson.ppf(p, mu=8)
q_norm = norm.ppf(p, loc=8, scale=np.sqrt(8))

fig = plt.figure(figsize=(6, 4))
plt.plot(q_norm, q_pois, "o")
plt.plot([min(q_norm), max(q_norm)], [min(q_norm), max(q_norm)], "r--")
plt.xlabel("Normal Quantiles")
plt.ylabel("Poisson Quantiles")
plt.title("QQ Plot: Poisson vs Normal Approximation")
plt.show()

# 2.
probs = [0.025, 0.05, 0.95, 0.975]
for p in probs:
    q_pois = poisson.ppf(p, mu=8)
    q_norm = norm.ppf(p, loc=8, scale=np.sqrt(8))
    print(
        f"p = {p:.3f} | Poisson quantile = {q_pois:.3f} | Normal quantile = {q_norm:.3f}"
    )
