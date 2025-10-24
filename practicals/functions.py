import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from scipy.stats import norm, t, chisquare


def qqplot_custom(data, dist, ax=None, title=None):
    n = len(data)

    if dist == "normal":
        sdist = stats.norm
        params = stats.norm.fit(data)
    elif dist == "gamma":
        sdist = stats.gamma
    elif dist == "exponential":
        sdist = stats.expon
    elif dist == "pareto":
        sdist = stats.pareto
    elif dist == "lognormal":
        sdist = stats.lognorm
    elif dist == "genextreme":
        sdist = stats.genextreme
    else:
        raise ValueError("Unsupported distribution")

    # 1. Sort data
    sample_q = np.sort(data)

    # 2. Compute plotting positions (probabilities)
    probs = np.array([(k - 0.5) / n for k in range(1, n + 1)])

    # 3. Compute theoretical quantiles
    params = sdist.fit(data)  # Fix location to 0
    theoretical_q = sdist.ppf(probs, *params)

    # 4. Add line through first and third quartiles
    q1_theor, q3_theor = np.percentile(theoretical_q, [25, 75])
    q1_sample, q3_sample = np.percentile(sample_q, [25, 75])
    slope = (q3_sample - q1_sample) / (q3_theor - q1_theor)
    intercept = q1_sample - slope * q1_theor

    # 5. Make the plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(theoretical_q, sample_q)
    ax.plot(
        theoretical_q, intercept + slope * theoretical_q, color="red", linestyle="--"
    )
    ax.set_xlabel("Theoretical Quantiles")
    ax.set_ylabel("Sample Quantiles")
    if title is not None:
        ax.set_title(title)


def random_dist(theta, n):
    if theta < -1 or theta > 1:
        raise ValueError("theta for this distribution should be in [-1, 1]")
    else:
        U = np.random.uniform(0, 1, n)
        if theta == 0:
            return 2 * U - 1
        else:
            return (-1 + np.sqrt(4 * U * theta + theta**2 - 2 * theta + 1)) / theta


def bernoulli_sim(n, p, nsim):
    hatp1 = np.zeros(nsim)
    hatp2 = np.zeros(nsim)

    for i in range(nsim):
        # Simulate n Bernoulli trials with probability p
        hatp1[i] = np.mean(np.random.binomial(1, p, n))  # formula for p_1
        hatp2[i] = (n * hatp1[i] + 1) / (n + 2)  # formula for p_2

    return pd.DataFrame({"hatp1": hatp1, "hatp2": hatp2})


def meanCI(x, quantile_d="normal", alpha=0.05, sigma2=None):
    x = np.asarray(x)
    n = len(x)

    if sigma2 is not None:
        # Known variance
        q = norm.ppf(1 - alpha / 2) / np.sqrt(n)
        CI = (x.mean() - q * np.sqrt(sigma2), x.mean() + q * np.sqrt(sigma2))
    else:
        # Unknown variance
        if quantile_d == "normal":
            q = norm.ppf(1 - alpha / 2) / np.sqrt(n)
        elif quantile_d == "t":
            q = t.ppf(1 - alpha / 2, df=n - 1) / np.sqrt(n)
        else:
            raise ValueError("quantile_d must be 'normal' or 't'")

        CI = (x.mean() - q * x.std(ddof=1), x.mean() + q * x.std(ddof=1))

    return CI


def sim_dices(n, alpha, p, nsim):
    prob_unbiased = np.array([0.579, 0.347, 0.074])  # expected for p = 1/6
    rejections = np.zeros(nsim, dtype=bool)

    for i in range(nsim):
        # Simulate 3 dice with possibly different probabilities of 'success'
        y1 = np.random.choice([1, 0], size=n, p=[p[0], 1 - p[0]])
        y2 = np.random.choice([1, 0], size=n, p=[p[1], 1 - p[1]])
        y3 = np.random.choice([1, 0], size=n, p=[p[2], 1 - p[2]])

        # Sum of successes across dice
        y = y1 + y2 + y3
        y = np.where(y == 3, 2, y)  # collapse category 3 into 2

        # Count occurrences of 0, 1, and 2
        counts = np.array([np.sum(y == k) for k in range(3)])

        # Chi-square goodness-of-fit test
        chi2_stat, p_value = chisquare(f_obs=counts, f_exp=n * prob_unbiased)
        rejections[i] = p_value < alpha

    # Proportion of rejections
    prop_rejection = np.mean(rejections)
    return prop_rejection
