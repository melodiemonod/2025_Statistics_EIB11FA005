import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.mosaicplot import mosaic

from functions import qqplot_custom

path_to_data = os.path.join("data", "french_salary.csv")

# Load data
salary = pd.read_csv(path_to_data, header=0)

# 1.
print(salary.describe())

# 2.
fig, ax = plt.subplots(nrows=3, figsize=(6, 10))
ax[0].boxplot([salary["salary_men"], salary["salary_women"]], labels=["Men", "Women"])
ax[0].set_ylabel("Hourly Salary")
ax[0].grid(axis="y", linestyle="--", alpha=0.7)

ax[1].hist(salary["salary_men"], bins=100, alpha=0.6, label="Men")
ax[1].hist(salary["salary_women"], bins=50, alpha=0.6, label="Women")
ax[1].set_xlabel("Hourly Salary")
ax[1].set_ylabel("Frequency")
ax[1].legend()
ax[1].grid(axis="y", linestyle="--", alpha=0.7)

sns.kdeplot(salary["salary_men"], fill=True, label="Men", bw_adjust=1.0, ax=ax[2])
sns.kdeplot(salary["salary_women"], fill=True, label="Women", bw_adjust=1.0, ax=ax[2])
ax[2].set_xlabel("Hourly Salary")
ax[2].set_ylabel("Density")
ax[2].legend()
ax[2].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()


# 3.


distributions = [
    "normal",
    "exponential",
    "gamma",
    "pareto",
    "lognormal",
    "genextreme",
]
labels = [
    "Normal",
    "Exponential",
    "Gamma",
    "Pareto",
    "Log-Normal",
    "Generalized Extreme Value",
]

#
# Men salary
data_men = salary["salary_men"]

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(14, 10))
for i, distribution in enumerate(distributions):
    label = labels[i]
    ax_column_index = i
    ax_row_index = 0
    if i > 2:
        ax_column_index -= 3
        ax_row_index = 1

    qqplot_custom(
        data_men,
        dist=distribution,
        title=f"{label} Distribution",
        ax=ax[ax_row_index, ax_column_index],
    )

#
# Women salary
data_women = salary["salary_women"]

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(14, 10))
for i, distribution in enumerate(distributions):
    label = labels[i]
    ax_column_index = i
    ax_row_index = 0
    if i > 2:
        ax_column_index -= 3
        ax_row_index = 1

    qqplot_custom(
        data_women,
        dist=distribution,
        title=f"{label} Distribution",
        ax=ax[ax_row_index, ax_column_index],
    )


# 4.
salary["relative_salary_gap"] = salary["salary_men"] / salary["salary_women"]

# Define bins (edges)
bins = [0, 1, 1.1, 1.2, 1.3, 1.5, 3]
labels = [
    "Lower",
    "Same-10% higher",
    "10-20% higher",
    "20-30% higher",
    "30-50% higher",
    ">50% higher",
]

# Create binned variable
salary["relative_salary_gap_binned"] = pd.cut(
    salary["relative_salary_gap"], bins=bins, labels=labels
)

# Frequency and relative frequncy tables
freq_tab = salary["relative_salary_gap_binned"].value_counts().sort_index()
print(freq_tab)

rfreq_tab = (
    salary["relative_salary_gap_binned"].value_counts(normalize=True).sort_index()
)
print(rfreq_tab)

# Plot
plt.figure(figsize=(10, 6))
rfreq_tab.plot(kind="bar")
plt.xlabel("Men's Salary Relative to Women's")
plt.ylabel("Proportion across French cities")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 5.

# Create binned variable
labels = ["Very Low", "Low", "Medium", "High", "Very High"]
salary["population_binned"], bin_edges = pd.qcut(
    salary["population"], q=5, labels=labels, retbins=True
)

# Contingency table
cont_tab = pd.crosstab(
    salary["population_binned"], salary["relative_salary_gap_binned"]
)
print(cont_tab)
cont_tab_index_norm = pd.crosstab(
    salary["population_binned"], salary["relative_salary_gap_binned"], normalize="index"
)
print(cont_tab_index_norm)

# sort dataset
salary_sorted = salary.sort_values("population_binned", ascending=False).sort_values(
    "relative_salary_gap_binned"
)

# plot
fig, ax = plt.subplots(figsize=(8, 6))
mosaic(
    salary_sorted,
    ["population_binned", "relative_salary_gap_binned"],
    labelizer=lambda key: "",
    ax=ax,
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()
