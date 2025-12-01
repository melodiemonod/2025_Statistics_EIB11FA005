import os
import pandas as pd
import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from functions import meanCI

#
# 2.1
#

# Data
x = np.array(
    [
        14.60,
        11.21,
        15.56,
        11.37,
        13.68,
        11.06,
        26.58,
        13.37,
        15.98,
        12.07,
        13.22,
        12.01,
        15.07,
    ]
)
sigma2 = 16  # known variance
n = len(x)

# 1. Confidence interval using known variance
CI_norm = meanCI(x, quantile_d="normal", alpha=0.05, sigma2=sigma2)  # using function

# 2. Confidence interval using unknown variance
CI_t = meanCI(x, quantile_d="t", alpha=0.05)  # using function


#
# 2.2
#

# 2.2.1
path_to_temperature_data = os.path.join("data", "daily_temperature_Paris.csv")
temperature = pd.read_csv(path_to_temperature_data, header=0)

temp_jan_2015 = temperature[
    (temperature["Month"] == 1) & (temperature["Year"] == 2015)
]["AvgTemperature"]
temp_feb_2015 = temperature[
    (temperature["Month"] == 2) & (temperature["Year"] == 2015)
]["AvgTemperature"]

fig = plt.figure(figsize=(6, 4))
plt.boxplot([temp_jan_2015, temp_feb_2015], labels=["January", "February"], notch=True)
plt.ylabel("Temperature (°C)")

# 2.2.2
path_to_data = os.path.join("data", "french_salary.csv")
salary = pd.read_csv(path_to_data, header=0)

fig = plt.figure(figsize=(8, 4))
plt.boxplot(
    [salary["salary_men"], salary["salary_women"]],
    labels=["Men", "Women"],
    notch=True,
    vert=False,
)
plt.xlabel("Hourly Salary")
plt.xscale("log")
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.gca().xaxis.set_minor_formatter(ScalarFormatter())


#
# 2.3
#

path_to_data = os.path.join("data", "parking.csv")
parking = pd.read_csv(path_to_data, header=0, sep=";")

# Separate data
brink = parking.loc[parking["BRINK"] == 1, "CONTR"]
other = parking.loc[parking["BRINK"] == 0, "CONTR"]

# 1. Exploratory analysis                              #

# ---------------- Histograms ----------------
xmin = min(min(brink), min(other))
xmax = max(max(brink), max(other))

fig, ax = plt.subplots(figsize=(10, 4), ncols=2, nrows=1)
ax[0].hist(brink, color="chocolate", edgecolor="black")
ax[0].set_xlabel("Collections per month ($) by Brink")
ax[0].set_ylabel("Frequency")
ax[0].set_xlim(xmin, xmax)
ax[1].hist(other, color="skyblue", edgecolor="black")
ax[1].set_xlabel("Collections per month ($) by other contractors")
ax[1].set_ylabel("Frequency")
ax[1].set_xlim(xmin, xmax)
plt.show()

# ---------------- Boxplots ----------------
fig = plt.figure(figsize=(6, 4))
plt.boxplot([brink, other], notch=True, labels=["Brink", "Other"])
plt.xlabel("Brink's contract")
plt.ylabel("Collections ($)")
plt.show()

# ---------------- Plots ----------------
fig = plt.figure(figsize=(6, 4))
plt.plot(parking["TIME"], parking["CONTR"], color="chocolate")
plt.xlabel("Months")
plt.ylabel("Collections by contractors ($)")
plt.axvline(x=12.5, linestyle="--", color="chocolate")
plt.axvline(x=36.5, linestyle="--", color="chocolate")
plt.text(
    25,
    2_100_000,
    "Brink's contract time",
    color="chocolate",
    verticalalignment="bottom",
)
plt.show()

# 2. Confidence intervals

# Statistics

n_brink = len(brink)
n_other = len(other)

sigma2_brink = np.var(brink, ddof=1)  # sample variance
sigma2_other = np.var(other, ddof=1)

mu_brink = np.mean(brink)
mu_other = np.mean(other)

alpha = 0.05

### Assuming variance is KNOWN

# Brink's workers
left_b, right_b = meanCI(brink, quantile_d="normal", alpha=alpha, sigma2=sigma2_brink)

# Other workers
left_c, right_c = meanCI(other, quantile_d="normal", alpha=alpha, sigma2=sigma2_other)

# Plot
fig = plt.figure(figsize=(6, 4))
plt.plot(parking["TIME"], parking["CONTR"], color="black")
plt.hlines(
    [left_b, mu_brink, right_b],
    xmin=parking["TIME"].min(),
    xmax=parking["TIME"].max(),
    colors="chocolate",
    linestyles=["--", "-", "--"],
    linewidth=2,
)
plt.hlines(
    [left_c, mu_other, right_c],
    xmin=parking["TIME"].min(),
    xmax=parking["TIME"].max(),
    colors="deepskyblue",
    linestyles=["--", "-", "--"],
    linewidth=1.5,
)
plt.legend(["Collections", "Brink Workers", "Other Workers"], loc="lower right")
plt.xlabel("Months")
plt.ylabel("Collections by contractors ($)")
plt.show()

### Assuming variance is UNKNOWN

# Brink
left_b, right_b = meanCI(brink, quantile_d="t", alpha=alpha)

# Other
left_c, right_c = meanCI(other, quantile_d="t", alpha=alpha)

# Plot
fig = plt.figure(figsize=(6, 4))
plt.plot(parking["TIME"], parking["CONTR"], color="black")
plt.hlines(
    [left_b, mu_brink, right_b],
    xmin=parking["TIME"].min(),
    xmax=parking["TIME"].max(),
    colors="chocolate",
    linestyles=["--", "-", "--"],
    linewidth=2,
)
plt.hlines(
    [left_c, mu_other, right_c],
    xmin=parking["TIME"].min(),
    xmax=parking["TIME"].max(),
    colors="deepskyblue",
    linestyles=["--", "-", "--"],
    linewidth=1.5,
)
plt.legend(["Collections", "Brink Workers", "Other Workers"], loc="lower right")
plt.xlabel("Months")
plt.ylabel("Collections by contractors ($)")
plt.show()

# Approximate CI for difference in means, equal variances
z = norm.ppf(1 - alpha / 2)
mu_diff = mu_brink - mu_other
s_diff = ((n_brink - 1) * sigma2_brink + (n_other - 1) * sigma2_other) / (
    n_brink + n_other - 2
)
error_diff = z * np.sqrt(s_diff * (1 / n_brink + 1 / n_other))
diffCI = (mu_diff - error_diff, mu_diff + error_diff)
print("Approximate CI, equal variances:", diffCI)

# Exact CI with t-distribution, equal variances
t_val = t.ppf(1 - alpha / 2, df=n_brink + n_other - 2)
error_diff = t_val * np.sqrt(s_diff * (1 / n_brink + 1 / n_other))
diffCI_t = (mu_diff - error_diff, mu_diff + error_diff)
print("Exact CI with t-distribution, equal variances:", diffCI_t)

# Approximate CI, unequal variances
s_diff_unequal = sigma2_brink / n_brink + sigma2_other / n_other
error_diff = z * np.sqrt(s_diff_unequal)
diffCI_uneq = (mu_diff - error_diff, mu_diff + error_diff)
print("Approximate CI, unequal variances:", diffCI_uneq)

# CI, unequal variances, t-distribution
df_min = min(n_brink - 1, n_other - 1)
t_val = t.ppf(1 - alpha / 2, df=df_min)
error_diff = t_val * np.sqrt(s_diff_unequal)
diffCI_uneq_t = (mu_diff - error_diff, mu_diff + error_diff)
print("CI, unequal variances, t-distribution:", diffCI_uneq_t)
