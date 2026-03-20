import numpy as np


def cycle(v, k):
    """Rotate vector left by k positions"""
    return np.roll(v, -k)


def intra_vector_sum(z):
    """
    Sums all elements of z using the fast log(N/2) method:
      - Cycle by 1, add → each slot gets pairs
      - Cycle by 2, add → each slot gets quads
      - Repeat for log2(N) steps
    Returns the full vector (every coordinate = sum).
    """
    v = z.copy().astype(float)
    N = len(v)
    step = 1
    while step < N:
        v = v + cycle(v, step)
        step *= 2
    return v


def vector_mean(z):
    """
    Computes the mean of all elements in z.
    Strategy: intra-vector sum → divide by N (known constant).
    Returns a scalar.
    """
    z = np.asarray(z, dtype=float)
    N = len(z)
    summed = intra_vector_sum(z)
    return summed[0] / N   # every slot is the sum


def dot_product(c, d):
    """
    Dot product via elementwise multiply then intra-vector sum.
    Demonstrates the 'dot product' consequence from the text.
    """
    c, d = np.asarray(c, dtype=float), np.asarray(d, dtype=float)
    return intra_vector_sum(c * d)[0]


# --- Demo ---
if __name__ == "__main__":
    z = np.array([3.0, 1.0, 4.0, 1.5, 9.0, 2.6, 5.0, 2.0])  # N=8 (2**3)

    print("Input:       ", z)
    print("Sum vector:  ", intra_vector_sum(z))   # every slot should equal sum
    print("Mean:        ", vector_mean(z))
    print("np.mean check", np.mean(z))

    # Dot product example
    c = np.array([1.0, 2.0, 3.0, 4.0, 0, 0, 0, 0])
    d = np.array([4.0, 3.0, 2.0, 1.0, 0, 0, 0, 0])
    print("\nDot product: ", dot_product(c, d))
    print("np check:    ", np.dot(c, d))