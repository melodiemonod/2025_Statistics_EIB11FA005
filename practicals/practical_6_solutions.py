import numpy as np

from functions import random_dist

# parameters
nsim = 1000
n = 10
theta = 1

# placeholder for sample means
xbar = []

np.random.seed(12345)

# loop over replications
for i in range(nsim):
    sample = random_dist(theta, n)

    # compute x bar
    xbar.append(np.mean(sample))

xbar = np.array(xbar)
thetahat = 3 * xbar

# count how many times condition holds
count = np.sum(thetahat > theta)

print(count)
