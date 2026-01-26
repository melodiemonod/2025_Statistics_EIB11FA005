import numpy as np
import pandas as pd
from scipy.stats import chisquare, binom
import matplotlib.pyplot as plt

from functions import sim_dices

# 2.1

# 1.
observed = np.array([48, 34, 15, 3])
n = 3  # number of dice
p = 1 / 6

# Expected frequencies for 0,1,2,3 sixes
expected_probs = binom.pmf(k=np.arange(0, n + 1), n=n, p=p)
expected = expected_probs * observed.sum()

chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
print(f"Chi2 = {chi2_stat}, p-value = {p_value}")

# 2.

n = 100
alpha = 0.05
nsim = 1000

# (1) Unbiased dice
p_fair = [1 / 6, 1 / 6, 1 / 6]
res_fair = sim_dices(n, alpha, p_fair, nsim)
print(f"(1) Fair dice (p=1/6): proportion of rejections = {res_fair:.3f}")

# (2) Biased dice
p_biased = [1 / 4, 1 / 4, 1 / 4]
res_biased = sim_dices(n, alpha, p_biased, nsim)
print(f"(2) Biased dice (p=1/4): proportion of rejections = {res_biased:.3f}")

# (3) Bonus: varying bias
prob_values = np.arange(0.16, 0.26, 0.01)
rejections = [sim_dices(n, alpha, [p, p, p], nsim) for p in prob_values]

plt.plot(prob_values, rejections, marker="o")
plt.xlabel("Dice success probability (p)")
plt.ylabel("Rejection rate")
plt.title("Empirical power of chi-square test vs bias level")
plt.grid(True)
plt.show()
