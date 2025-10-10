import os

import pandas as pd
import numpy as np

path_to_data = os.path.join("data", "daily_temperature_Paris.csv")

# Read data
df = pd.read_csv(path_to_data, header=0)

#
# 1.2
#


# Subset to January 2015
jan_2015 = df[(df["Month"] == 1) & (df["Year"] == 2015)]["AvgTemperature"].round(2)

# Sorting
jan_2015 = np.sort(jan_2015)
print("January Data: ", jan_2015)

# Measures of center
jan_2015_mean = np.mean(jan_2015)
jan_2015_median = np.median(jan_2015)
print("Mean January:", jan_2015_mean)
print("Median January:", jan_2015_median)

# Measures of dispersion
jan_2015_range = np.max(jan_2015) - np.min(jan_2015)
jan_2015_iqr = np.quantile(jan_2015, 0.75) - np.quantile(jan_2015, 0.25)
jan_2015_var = np.var(jan_2015, ddof=1)  # Sample variance
jan_2015_std = np.std(jan_2015, ddof=1)  # Standard deviation
print("Range Janaury", jan_2015_range)
print("Std Janaury", jan_2015_std)
print("IQR January:", jan_2015_iqr)

# 12th Quantiles
jan_2015_quantile_12 = np.quantile(jan_2015, 0.12)
print("12th quantile January:", jan_2015_quantile_12)

#
# 1.3
#

# Subset to February 2015
feb_2015 = df[(df["Month"] == 2) & (df["Year"] == 2015)]["AvgTemperature"]

# Measures of center
feb_2015_mean = np.mean(feb_2015)
feb_2015_median = np.median(feb_2015)
print("Mean February:", feb_2015_mean)
print("Median February:", feb_2015_median)

# Measures of dispersion
feb_2015_range = np.max(feb_2015) - np.min(feb_2015)
feb_2015_iqr = np.percentile(feb_2015, 75) - np.percentile(feb_2015, 25)
feb_2015_var = np.var(feb_2015, ddof=1)  # Sample variance
feb_2015_std = np.std(feb_2015, ddof=1)  # Standard deviation
print("Std February", feb_2015_std)
print("IQR February:", feb_2015_iqr)
