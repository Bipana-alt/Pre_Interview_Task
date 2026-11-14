import numpy as np
import matplotlib.pyplot as plt

# Error bounds used in our experiments
error_bounds = ["1e-2", "1e-3", "1e-4", "1e-5", "1e-6"]

# Compression ratios reported by SZ3
compression_ratios = np.array([
    939.558220,
    118.030867,
    22.175211,
    8.493128,
    4.933390
])

# PSNR values reported by SZ3 (dB)
psnr = np.array([
    53.407718,
    69.279266,
    86.171536,
    104.771242,
    125.575613
])

# Calculate bitrate using the assignment formula
bitrate = 32 / compression_ratios

# Create the plot
plt.figure(figsize=(8, 5))

plt.plot(
    bitrate,
    psnr,
    marker="o",
    linewidth=2,
    markersize=7,
    color="darkred"
)

# Label each point with its error bound
for x, y, bound in zip(bitrate, psnr, error_bounds):
    plt.annotate(
        bound,
        (x, y),
        xytext=(6, 6),
        textcoords="offset points"
    )

plt.xlabel("Bitrate (bits/value)")
plt.ylabel("PSNR (dB)")
plt.title("SZ3 Rate-Distortion Performance on Hurricane ISABEL Pressure Data")

plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

# Save the figure
plt.savefig("rate_distortion.png", dpi=300)
plt.savefig("rate_distortion.pdf")

print("Rate-distortion plots saved successfully!")

# Display calculated bitrate values
for bound, rate in zip(error_bounds, bitrate):
    print(f"{bound}: {rate:.6f} bits/value")
