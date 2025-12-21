import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import t, wilcoxon, ttest_1samp

from functions import qqplot_custom

path_to_data = os.path.join("data", "DrugsUsage.csv")
drugs = pd.read_csv(path_to_data, header=0)

#
# Theoretical exercises
#

# Exercise 1
# 4.

t.cdf(x=-1.78, df=9)

#
# Python Application
#


# 2.1

# 1.
drugs.dropna(subset=["CIGTRY"], inplace=True)

# 2.
qqplot_custom(drugs["CIGTRY"], dist="normal")

# 3.
mu_0 = 15.5

t_obs_wilcoxon, p_value_wilcoxon = wilcoxon(
    drugs["CIGTRY"] - mu_0, alternative="two-sided"
)
print("Wilcoxon test: t_obs =", t_obs_wilcoxon, ", p-value =", p_value_wilcoxon)

# 4.

t_obs, p_value = ttest_1samp(drugs["CIGTRY"], popmean=mu_0, alternative="two-sided")
print("t-test: t_obs =", t_obs, ", p-value =", p_value)

# 5.
t_obs_wilcoxon, p_value_wilcoxon = wilcoxon(
    drugs["CIGTRY"] - mu_0, alternative="greater"
)
print(
    "Wilcoxon test, alternative greater: t_obs =",
    t_obs_wilcoxon,
    ", p-value =",
    p_value_wilcoxon,
)
