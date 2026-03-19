import numpy as np


# --- Sign building blocks ---

def sign_0_1(x):
    """Sign_{0,1,0}(x): returns 0 if x<0, 0.5 if x=0, 1 if x>0."""
    return np.where(x > 0, 1, np.where(x < 0, 0, 0.5))

def sign_neg1_1(x):
    """Sign_{-1,1,0}(x): returns -1 if x<0, 0 if x=0, 1 if x>0."""
    return np.sign(x)


# --- Fuzzy equality ---

def fuzzy_equal_zero(x, epsilon=0.01):
    """Returns 1 where x ≈ 0, else 0. Works componentwise on arrays."""
    x = np.asarray(x, dtype=float)
    return ((x >= -epsilon) & (x <= epsilon)).astype(int)


# --- Median (Method 1) ---

def median_position(z, epsilon=0.01):
    """
    Returns a 0-1 vector indicating which position(s) hold the median.

    Steps:
      1. Build D where D[i,j] = Sign_{-1,1,0}(z_i - z_j)
         (diagonal is 0 by definition of the sign function at 0)
      2. Sum each row  →  m_i = sum_j D[i,j]
         The median row sums to 0 (equal # of -1s and +1s)
      3. Apply fuzzy equality with 0  →  0-1 mask
    """
    z = np.asarray(z, dtype=float)
    # Step 1: D[i,j] = sign(z_i - z_j)
    D = sign_neg1_1(z[:, None] - z[None, :])   # shape (N, N)
    # Step 2: row sums
    row_sums = D.sum(axis=1)                    # shape (N,)
    # Step 3: fuzzy equality with 0
    mask = fuzzy_equal_zero(row_sums, epsilon=epsilon)
    return mask

def median_value(z, epsilon=0.01):
    """
    Returns the median value via Sum(m * z).
    Note: only correct when exactly one element is the median
    (i.e. N is odd and all values are distinct — as the textbook assumes).
    """
    z = np.asarray(z, dtype=float)
    m = median_position(z, epsilon=epsilon)
    return np.sum(m * z)


if __name__ == "__main__":
    z = np.array([3.0, 1.0, 4.0, 1.5, 9.0, 2.6, 5.0])  # N= odd length

    mask = median_position(z)
    print("Input:    ", z)
    print("Mask:     ", mask)
    print("Position: ", np.where(mask)[0])
    print("Value:    ", median_value(z))
    print("np check: ", np.median(z))      