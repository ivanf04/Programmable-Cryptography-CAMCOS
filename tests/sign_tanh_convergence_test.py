import csv
import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_tanh

# 1. Create your sample set (-2.000 to 2.000)
xs = [i / 1000 for i in range(-2000, 2000)]

# 2. Steepness values to sweep
k_values = [1, 2, 4, 8, 16, 32, 64]

# Long ("tidy") format: one row per (k, x) pair, with k as its own column.
# In Plotly this lets you do px.line(df, x="x_value", y="tanh_approximation",
# color="k") to get one filterable trace per k.
with open("sign_tanh_convergence_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file)

    # add header
    writer.writerow(["k", "x_value", "tanh_approximation", "sign_real"])

    print("Starting FHE computations and saving to CSV...")

    for k in k_values:
        print(f"  Computing k = {k} ...")

        for test_val in xs:
            # calculate the true sign value of input values
            if test_val < 0:
                sign_real = 0.0
            elif test_val == 0:
                sign_real = 0.5
            else:
                sign_real = 1.0

            # Ciphertext preparation loop
            z_vals = [test_val] * 8
            z = Ciphertext(8)
            for idx, val in enumerate(z_vals):
                z.set_element(idx, val)

            # Run FHE Evaluation
            tanh_result = sign_tanh(
                z, a=0, b=1, c=0, k=k, n_terms=9
            )

            # extract the clean, real numeric output
            real_output = np.real(tanh_result[0])

            # write all values into the CSV file
            writer.writerow([k, test_val, real_output, sign_real])


print("Done! File saved as 'sign_tanh_convergence_results.csv'")
