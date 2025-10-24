import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

path_to_psg_data = os.path.join("data", "psg_insights.csv")
path_to_temperature_data = os.path.join("data", "daily_temperature_Paris.csv")

# Load data
psg = pd.read_csv(path_to_psg_data, header=0)
psg.head()

#
# 1. Exercise 1: Tables
#

# 1.
scored_goals = psg["ScoredGoals"].value_counts().sort_index()
conceded_goals = psg["ConcededGoals"].value_counts().sort_index()
print("Scored Goals:", scored_goals)
print("Conceded Goals:", conceded_goals)

# 2.
scored_goals_rfreq = psg["ScoredGoals"].value_counts(normalize=True).sort_index()
conceded_goals_rfreq = psg["ConcededGoals"].value_counts(normalize=True).sort_index()
print("Scored Goals:", scored_goals_rfreq)
print("Conceded Goals:", conceded_goals_rfreq)

# 2.a
n_match = len(psg)
print("Scored 4 goals:", sum(psg["ScoredGoals"] == 4) / n_match)

# 2.b
print("Conceded more than 1 goal:", sum(psg["ConcededGoals"] > 1) / n_match)

# 3.
print(pd.crosstab(psg["HomeMatch"], psg["Winner"]))

# 3.a
print(
    "Number of home match lost:",
    sum((psg["Winner"] == False) & (psg["HomeMatch"] == True)),
)

# 3.b
print("Probability to win a match:", sum(psg["Winner"] == True) / n_match)

# 3.c
n_home_match = sum(psg["HomeMatch"] == True)
print(
    "Probability to win a home match:",
    sum((psg["Winner"] == True) & (psg["HomeMatch"] == False)) / n_home_match,
)

# 3.d
print("Probability of away match:", sum(psg["HomeMatch"] == False) / n_match)
print("Probability to lose a match:", sum(psg["Winner"] == False) / n_match)
print(
    "Number of away match lost:",
    sum((psg["Winner"] == False) & (psg["HomeMatch"] == False)),
)

#
# 2. Barplot / Histogram for Discrete Numerical Data
#

# 1.
plt.figure(figsize=(6, 6))
plt.hist(psg["ScoredGoals"])
plt.show()

plt.figure(figsize=(6, 6))
plt.hist(psg["ScoredGoals"], bins=range(8), align="left")
plt.xlabel("ScoredGoals")
plt.ylabel("Count")
plt.show()

# 2.
plt.figure(figsize=(6, 6))
psg["ScoredGoals"].value_counts().plot.bar()
plt.show()

plt.figure(figsize=(6, 6))
psg["ScoredGoals"].value_counts().reindex(range(7), fill_value=0).plot.bar()
plt.show()

# 3.
plt.figure(figsize=(6, 6))
psg["ScoredGoals"].value_counts().reindex(range(7), fill_value=0).plot.barh()
plt.title("Goals Scored by PSG")
plt.show()


#
# 3. Plots for continuous Numerical Data
#


# Read data
df = pd.read_csv(path_to_temperature_data, header=0)

# Subset to January / february 2015
temp_2015 = df[(df["Month"] <= 2) & (df["Year"] == 2015)]

# 2.
jan_2015 = temp_2015[(temp_2015["Month"] == 1)]
plt.figure(figsize=(5, 4))
sns.boxplot(
    x="Month",
    y="AvgTemperature",
    data=jan_2015,
    medianprops=dict(color="black"),
    boxprops=dict(facecolor="white"),
)
plt.xticks([])
plt.title("Temperatures in January 2015")
plt.tight_layout()
plt.show()

# 3.
plt.figure(figsize=(6, 5))
sns.boxplot(
    x="Month",
    y="AvgTemperature",
    data=temp_2015,
    medianprops=dict(color="black"),
    boxprops=dict(facecolor="white"),
)
plt.xticks([0, 1], ["January", "February"])
plt.title("Comparison of January and February 2015")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()

# 4.
plt.figure(figsize=(6, 5))
sns.violinplot(
    x="Month",
    y="AvgTemperature",
    data=temp_2015,
)
plt.xticks([0, 1], ["January", "February"])
plt.title("Comparison of January and February 2015")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()

# 5.
plt.figure(figsize=(4, 3))
sns.kdeplot(jan_2015["AvgTemperature"], fill=True)
plt.xlabel("Temperature (°C) in January 2015")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

bw_adjust = 0.5
plt.figure(figsize=(4, 3))
sns.kdeplot(
    jan_2015["AvgTemperature"],
    bw_adjust=bw_adjust,
    fill=True,
)  # smaller bw -> less smooth
plt.xlabel("Temperature (°C) in January 2015")
plt.ylabel("Density")
plt.title("bw_adjust = 0.5")
plt.tight_layout()
plt.show()

bw_adjust = 1.5
plt.figure(figsize=(4, 3))
sns.kdeplot(
    jan_2015["AvgTemperature"],
    bw_adjust=bw_adjust,
    fill=True,
)  # smaller bw -> less smooth
plt.xlabel("Temperature (°C) in January 2015")
plt.ylabel("Density")
plt.title("bw_adjust = 1.5")
plt.tight_layout()
plt.show()


#
# Exercise 4: QQ plot
#


# 1.
def qqplot_custom(data, dist):
    n = len(data)

    # (a) Sort data
    sample_q = np.sort(data)

    # (b) Compute plotting positions (probabilities)
    probs = np.array([(k - 0.5) / n for k in range(1, n + 1)])

    # (c) Compute theoretical quantiles
    if dist == "normal":
        params = stats.norm.fit(data)
        theoretical_q = stats.norm.ppf(probs, *params)
    elif dist == "poisson":
        params = (np.mean(data),)
        theoretical_q = stats.poisson.ppf(probs, *params)

    # (d) Add line through first and third quartiles
    q1_theor, q3_theor = np.percentile(theoretical_q, [25, 75])
    q1_sample, q3_sample = np.percentile(sample_q, [25, 75])
    slope = (q3_sample - q1_sample) / (q3_theor - q1_theor)
    intercept = q1_sample - slope * q1_theor

    # (e) Make the plot
    plt.figure(figsize=(6, 6))
    plt.scatter(theoretical_q, sample_q, label="Quantiles")
    plt.plot(
        theoretical_q,
        intercept + slope * theoretical_q,
        color="red",
        linestyle="--",
        label="Diagonal line",
    )
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")
    plt.title("Custom Q-Q Plot")
    plt.legend()
    plt.show()


# 2.
data = jan_2015["AvgTemperature"]
qqplot_custom(data=data, dist="normal")

# 3.
data = psg["ScoredGoals"]
qqplot_custom(data=data, dist="poisson")
