import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, poisson
import seaborn as sns

from functions import qqplot_custom

#
# Distributions in Python
#

# 1.
mu, sigma = 10, 2
p1 = norm.cdf(12, loc=mu, scale=sigma)
p2 = norm.cdf(12, loc=mu, scale=sigma) - norm.cdf(10, loc=mu, scale=sigma)
print(p1, p2)

# 2.
rate = 0.5
q90 = expon.ppf(0.9, scale=1 / rate)
print(q90)

# 3.
lam = 4
p_eq2 = poisson.pmf(2, mu=lam)
p_lt2 = poisson.cdf(1, mu=lam)
print(p_eq2, p_lt2)

# 4.
sample = norm.rvs(loc=1.5, scale=2, size=200)

fig = plt.figure(figsize=(6, 6))
plt.hist(sample, density=True, alpha=0.5, label="Sample")
x = np.linspace(min(sample), max(sample), 100)
plt.plot(x, norm.pdf(x, loc=1.5, scale=2), "r-", lw=2, label="PDF")
plt.legend()
plt.show()

#
# Sampling Distribution of the Median
#

# 2.

np.random.seed(12)

lam = 1 / 2
medians = []
for i in range(500):
    sample = np.random.exponential(scale=1 / lam, size=100)
    medians.append(np.median(sample))

medians = np.array(medians)

# 2.a

params = norm.fit(medians)

fig = plt.figure(figsize=(6, 6))
plt.hist(medians, bins=20, density=True, alpha=0.5)
x = np.linspace(min(medians) - 0.5, max(medians), 100)
plt.xlim(min(medians) - 0.5, max(medians))
plt.plot(
    x, norm.pdf(x, loc=params[0], scale=params[1]), "r-", lw=2, label="PDF Normal Fit"
)
plt.title("Sampling distribution of the median")
plt.show()

fig, ax = plt.subplots(figsize=(10, 6), nrows=1, ncols=2)
sns.histplot(medians, kde=True, ax=ax[0])
sns.boxplot(x=medians, ax=ax[1])
plt.title("Sampling distribution of the median")
plt.show()

# 2.b
qqplot_custom(data=medians, dist="normal")
