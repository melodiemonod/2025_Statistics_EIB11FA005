import os
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, f_oneway, kruskal
import matplotlib.pyplot as plt
import seaborn as sns

from functions import qqplot_custom

#
# 2.1
#

path_to_data = os.path.join("data", "DrugsUsage.csv")
drugs = pd.read_csv(path_to_data, header=0)

# Remove missing values
cigtry = drugs["CIGTRY"].dropna()
alctry = drugs["ALCTRY"].dropna()

# Check normality
qqplot_custom(cigtry, dist="normal", title="CIGTRY")
qqplot_custom(alctry, dist="normal", title="ALCTRY")

# Check variance
var_cigtry, var_alctry = cigtry.var(), alctry.var()
print("Variance CIGTRY:", var_cigtry)
print("Variance ALCTRY:", var_alctry)

# Paired t-test if normal, Wilcoxon if not
t_obs, p_value = mannwhitneyu(cigtry, alctry, alternative="two-sided")
print("Wilcoxon test: t_obs =", t_obs, ", p-value =", p_value)

#
# 2.2
#

path_to_data = os.path.join("data", "coagulation.csv")
times = pd.read_csv(path_to_data, header=0)

# 1.

# Split data by diet group
groups = [times["coag"][times["diet"] == d] for d in times["diet"].unique()]

# Perform one-way ANOVA
f_stat, p_value = f_oneway(*groups)

print("F-statistic:", f_stat)
print("p-value:", p_value)

# 2.

# checking the same variance
plt.figure(figsize=(6, 5))
sns.boxplot(x="diet", y="coag", data=times)
plt.title("Boxplot of coag by diet")
plt.xlabel("Diet")
plt.ylabel("Coag")
plt.show()

# checking the normality assumption
qqplot_custom(
    times["coag"],
    "normal",
    title=f"QQ plot Diet",
)

# 3.

# Perform Kruskal-Wallis test
h_stat, p_value_kruskal = kruskal(*groups)

print("H-statistic:", h_stat)
print("p-value kruskal:", p_value_kruskal)
