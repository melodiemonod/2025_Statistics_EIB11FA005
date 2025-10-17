import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

path_to_gardasil_data = os.path.join("data", "GardasilStudy.csv")
path_to_contribution_data = os.path.join("data", "ContributionLite.csv")


#
# 1. Exercise 1
#

gardasil = pd.read_csv(path_to_gardasil_data, sep=";", header=0)
gardasil.head()

gardasil["Race"] = gardasil["Race"].astype("category")
gardasil["LocationType"] = gardasil["LocationType"].astype("category")
gardasil["InsuranceType"] = gardasil["InsuranceType"].astype("category")
gardasil["Completed"] = (
    gardasil["Completed"].map({1: "Completed", 0: "Uncompleted"}).astype("category")
)

# 1.
value_count_race = gardasil["Race"].value_counts()
value_count_completed = gardasil["Completed"].value_counts()
value_count_location = gardasil["LocationType"].value_counts()
value_count_insurance = gardasil["InsuranceType"].value_counts()

print("Value count Race:", value_count_race)
print("Value count Completed:", value_count_completed)
print("Value count Location:", value_count_location)
print("Value count Insurance:", value_count_insurance)

# 2.
gardasil.value_counts()

# 3.
proportions = gardasil["InsuranceType"].value_counts(normalize=True)

# 3.a
p_private = proportions["Private"]
print("Private Insurance proportion:", p_private)

# 3.b
p_non_public = 1 - proportions["Public"]
print("Non-public Insurance proportion:", p_non_public)

# 4.
cross_proportions = pd.crosstab(gardasil["InsuranceType"], gardasil["LocationType"])
n = cross_proportions.values.sum()

# 4.a
n_suburban = cross_proportions["Suburban"].sum()
print("Patients in suburban clinics:", n_suburban)

# 4.b
n_urban = cross_proportions["Urban"].sum()
p_urban = n_urban / n
print("Probability of going to an urban clinic:", p_urban)

# 4.c
n_private_suburban = cross_proportions.loc["Private"]["Suburban"]
p_private_suburban = n_private_suburban / n
print(
    "Probability of going to an urban clinic and private insurance:", p_private_suburban
)

# 4.d
n_military = cross_proportions.loc["Military"].sum()
n_military_urban = cross_proportions.loc["Military"]["Urban"]
p_urban_given_military = n_military_urban / n_military
print("Probability of urban clinic given military insurance:", p_urban_given_military)

# 5.
pd.crosstab(
    [gardasil["Race"], gardasil["Completed"]],
    [gardasil["InsuranceType"], gardasil["LocationType"]],
)

# 6.
print(
    "Patients in urban clinics with private insurance: ",
    cross_proportions.loc["Private"]["Urban"],
)


#
# 2. Exercise 2
#

#
# 2.1

# 2.
fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(autopct="%1.1f%%")
plt.show()

# 3.
fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(autopct="%1.1f%%")
plt.ylabel("")
plt.show()

# 4.
fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(autopct="%1.1f%%", radius=1.2)
plt.ylabel("")
plt.title("radius=1.2")
plt.show()

fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
plt.ylabel("")
plt.title("startangle=90")
plt.show()

# 5.
fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(
    autopct="%1.1f%%", colors=["Blue", "Red", "Green", "Yellow"]
)
plt.ylabel("")
plt.show()

fig = plt.figure()
gardasil["Race"].value_counts().plot.pie(
    autopct="%1.1f%%", colors=["Blue", "Red", "Green"]
)  # If the list of colors is shorter than the number of slices, Matplotlib will cycle through them.
plt.ylabel("")
plt.show()


#
# 2.2 Barplot

# 1.
fig = plt.figure()
gardasil["InsuranceType"].value_counts().plot.bar()
plt.show()

# 2.
fig = plt.figure()
gardasil["InsuranceType"].value_counts().plot.bar()
plt.title("Patients by type of insurance")
plt.show()

# 3.
fig = plt.figure(figsize=(6, 6))
gardasil["InsuranceType"].value_counts().plot.bar()
plt.title("Patients by type of insurance")
plt.tight_layout()
plt.show()

# 4.
fig = plt.figure(figsize=(6, 6))
gardasil["InsuranceType"].value_counts().plot.barh()
plt.title("Patients by type of insurance")
plt.tight_layout()
plt.show()

#
# 2.3 Mosaic plot

# 1.
mosaic(gardasil, ["Completed", "LocationType"])
plt.tight_layout()
plt.show()

# 2.
fig, ax = plt.subplots(figsize=(10, 6))
mosaic(gardasil, ["Completed", "LocationType"], ax=ax)
plt.tight_layout()
plt.show()

# 3.
fig, ax = plt.subplots(figsize=(10, 6))
mosaic(gardasil, ["LocationType", "Completed"], ax=ax)
plt.tight_layout()
plt.show()

# 4.
mosaic(
    gardasil,
    ["LocationType", "InsuranceType", "Completed"],
    labelizer=lambda key: "",
)
plt.tight_layout()
plt.show()

#
# 3. Exercise 3
#

ContributionLite = pd.read_csv(path_to_contribution_data, header=0)

# 1.

# Frequency of contributions by sector
sector_freq = ContributionLite["BroadSector"].value_counts()
print(sector_freq)

# Relative Frequency of contributions by sector
sector_rfreq = ContributionLite["BroadSector"].value_counts(normalize=True)
print(sector_rfreq)

# Bar plot of contributions by sector
plt.figure(figsize=(10, 8))
sector_freq.plot(kind="bar")
plt.title("Contribution by Sector")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 2.

# Frequency of contributions by party
party_freq = ContributionLite["GeneralParty"].value_counts()
print(party_freq)

# Relative Frequency of contributions by party
party_rfreq = ContributionLite["GeneralParty"].value_counts(normalize=True)
print(party_rfreq)

# Pie chart of contributions by party
plt.figure(figsize=(8, 8))
party_freq.plot(kind="pie", autopct="%1.1f%%")
plt.title("Contribution by Party")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 3.

# Contingency table of BroadSector vs GeneralParty
cont_tab = pd.crosstab(
    ContributionLite["BroadSector"],
    ContributionLite["GeneralParty"],
    normalize="index",
)
print(cont_tab)

# Mosaic plot
fig, ax = plt.subplots(figsize=(8, 6))
mosaic(
    ContributionLite, ["BroadSector", "GeneralParty"], labelizer=lambda key: "", ax=ax
)
plt.title("Contribution by Sector and Party")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()
