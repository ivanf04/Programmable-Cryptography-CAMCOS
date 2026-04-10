import sys
import numpy as np
from fhelib.stats.mode import mode
from fhelib.stats.fhe_median import median_value, median_position
from fhelib.stats.fhe_mean import vector_mean
"""
boiler plate for the "big test" file
"""
# big test file goes here 
def main():
    n = 2**5
    rng = np.random.default_rng(seed=42)
    data = rng.integers(low=0, high=1000, size=n, dtype=np.int64)

    true_mean = np.mean(data)
    true_median = np.median(data)
    values, counts = np.unique(data, return_counts=True)
    true_mode = values[np.argmax(counts)]

    print("ndarray:")
    print(data)
    print()

    print(f"True mean:   {true_mean}")
    print(f"True median: {true_median}")
    print(f"True mode:   {true_mode}")

    
    fhe_mean_result = vector_mean(data)
    fhe_median_result = median_position(data)
    fhe_mode_result = mode(data)

    print(f"FHE mean:    {fhe_mean_result}")
    print(f"FHE median:  {fhe_median_result}")
    print(f"FHE mode:    {fhe_mode_result}")

    print("\nComparisons:")
    print("Mean match:", np.isclose(fhe_mean_result, true_mean))
    print("Median match:", fhe_median_result == true_median)
    print("Mode match:", fhe_mode_result == true_mode)


if __name__ == "__main__":
    sys.exit(main())