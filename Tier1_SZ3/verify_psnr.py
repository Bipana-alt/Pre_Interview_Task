import numpy as np

# Step 1: Load original and decompressed data
original = np.fromfile("data/Pf48.bin.f32", dtype=np.float32)
reconstructed = np.fromfile("data/decompressed_1e-3.f32", dtype=np.float32)

# Step 2: Verify both files contain the same number of values
print("Original values:", original.size)
print("Reconstructed values:", reconstructed.size)

assert original.size == reconstructed.size == 25_000_000

# Step 3: Calculate the original data range
data_range = float(np.max(original)) - float(np.min(original))

# Step 4: Calculate Mean Squared Error (MSE)
difference = original.astype(np.float64) - reconstructed.astype(np.float64)
mse = np.mean(difference ** 2)

# Step 5: Calculate PSNR
psnr = 20 * np.log10(data_range) - 10 * np.log10(mse)

# Step 6: Compare with SZ3's reported PSNR
sz3_psnr = 69.279266
discrepancy = abs(psnr - sz3_psnr)

print("Data range:", data_range)
print("MSE:", mse)
print("Calculated PSNR:", psnr, "dB")
print("SZ3 PSNR:", sz3_psnr, "dB")
print("Discrepancy:", discrepancy, "dB")

if discrepancy < 0.001:
    print("PASS: Independent PSNR verification successful!")
else:
    print("FAIL: PSNR discrepancy exceeds 0.001 dB")
