import csv
import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_finite_k_scaled

# 1. Create your sample set (-0.414 to 0.414)
xs = [i / 1000 for i in range(-414, 415)]

# 2. Open a new CSV file to write data
with open("sigmoid_convergence_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # 3. Added "sign_real" to the header row
    writer.writerow(["x_value", "sigmoid_approximation", "sign_real"])
    
    print("Starting FHE computations and saving to CSV...")
    
    for test_val in xs:
        # --- Calculate the ideal sign_real value ---
        if test_val < 0:
            sign_real = 0.0
        elif test_val == 0:
            sign_real = 0.5
        else:
            sign_real = 1.0
        # -------------------------------------------

        # Your ciphertext preparation loop
        z_vals = [test_val] * 8
        z = Ciphertext(8)
        for idx, val in enumerate(z_vals):
            z.set_element(idx, val)

        # Run the FHE evaluation
        sigmoid_result = sign_finite_k_scaled(z, k=10.0, power=1, tol=1e-6)
        
        # 4. Extract the clean, real numeric part
        real_output = np.real(sigmoid_result[0])
        
        # 5. Write all three values directly into the CSV file
        writer.writerow([test_val, real_output, sign_real])
        
        # Optional: Print to console so you can watch progress
        # print(f"Processed x = {test_val:.3f} -> approx: {real_output:.4f}, real: {sign_real}")

print("Done! File saved as 'sigmoid_convergence_results.csv'")






