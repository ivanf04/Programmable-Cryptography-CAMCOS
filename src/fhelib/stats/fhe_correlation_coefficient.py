import numpy as np
from src.fhelib.stats.fhe_mean import vector_mean, intra_vector_sum


def demean(z):
    """
    Subtract mean from every element z = (z1-zu, z2-zu, ..., zN-zu)
    This is: z + (-1, -1, ..., -1) * zu
    """
    z = np.asarray(z, dtype=float)
    z_bar = vector_mean(z)         
    return z - z_bar


def correlation_coefficient(x, y):
    """
    Pearson r = Σ(xi - x̄)(yi - ȳ) / sqrt(Σ(xi-x̄)**2 · Σ(yi-ȳ)**2)

    Steps (following the text):
      1. Compute x'=demean(x)  and  y'=demean(y)
      2. Numerator = intra_vector_sum(x' * y')
      3. Denominator = sqrt(sum((x')**2) * sum((y')**2))
      4. Divide
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)

    # 1. Compute x'=demean(x)  and  y'=demean(y)
    x_prime = demean(x)
    y_prime = demean(y)

    # 2. Numerator = intra_vector_sum(x' * y')
    numerator = intra_vector_sum(x_prime * y_prime)[0]

    # 3. Denominator = sqrt(sum((x')**2) * sum((y')**2))
    sum_xx = intra_vector_sum(x_prime ** 2)[0]
    sum_yy = intra_vector_sum(y_prime ** 2)[0]
    denominator = np.sqrt(sum_xx * sum_yy)

    return numerator / denominator # ask about this


def coefficient_of_determination(x, y):
    """correlation coefficient squared"""
    r = correlation_coefficient(x, y)
    return r ** 2


def regression_coefficient(x, y):
    """
    β = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)**2

      1. Compute x'=demean(x)  and  y'=demean(y)
      2. Numerator = intra_vector_sum(x' * y')
      3. Denominator = sum((x')**2) 


    Same numerator as r, but denominator is just sum(x'**2) — no sqrt, no y term.
    """
    
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    
    # 1. Compute x'=demean(x)  and  y'=demean(y)
    x_prime = demean(x)
    y_prime = demean(y)

    # 2. Numerator = intra_vector_sum(x' * y')
    numerator   = intra_vector_sum(x_prime * y_prime)[0]

    # 3. Denominator = sum((x')**2) 
    denominator = intra_vector_sum(x_prime ** 2)[0]

    return numerator / denominator


# --- Demo ---
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    x = rng.uniform(0, 10, 8)
    y = 2.5 * x + rng.normal(0, 1, 8)   # y is roughly linear in x

    print("x:", x)
    print("y:", y)
    print()
    print("r:       ", correlation_coefficient(x, y))
    print("np check:", np.corrcoef(x, y)[0, 1])
    print()
    print("r**2:      ", coefficient_of_determination(x, y))
    print()
    print("β:       ", regression_coefficient(x, y))
    np_beta = np.cov(x, y)[0, 1] / np.var(x, ddof=1)
    print("np check:", np_beta)