import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

#
# 2.1
#

# 1.
data = np.array([[220, 55], [470, 253], [45, 39], [209, 122]])
chi2, p, dof, expected = chi2_contingency(data)
print(f"Chi2 = {chi2}, p-value = {p}")

# 2.

# Define row and column labels
rows = ["Public", "Private", "Hospitalization-only", "Military"]
cols = ["Not Completed", "Completed"]

# Convert to a DataFrame for clarity
df = pd.DataFrame(data, index=rows, columns=cols)

# Reshape into a long format suitable for mosaic()
mosaic_data = {(row, col): df.loc[row, col] for row in df.index for col in df.columns}

# Plot
plt.figure(figsize=(8, 6))
mosaic(mosaic_data, title="Mosaic Plot of Completion by Institution Type", gap=0.02)
plt.xlabel("Institution Type")
plt.ylabel("Proportion (Completed vs Not Completed)")
plt.show()
