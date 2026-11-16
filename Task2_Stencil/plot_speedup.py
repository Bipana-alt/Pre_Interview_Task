import matplotlib.pyplot as plt

# Number of OpenMP threads
threads = [1, 2, 4, 8]

# Median execution times from five trials
times = [3.1473, 1.9421, 1.1698, 0.9928]

# Calculate speedup relative to 1 thread
speedup = [times[0] / t for t in times]

# Ideal linear speedup
ideal = threads

# Create the plot
plt.figure(figsize=(7, 5))

plt.plot(threads, speedup, "o-", label="Measured speedup")
plt.plot(threads, ideal, "--", label="Ideal linear speedup")

plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.title("OpenMP Stencil Scaling")
plt.xticks(threads)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("speedup.png", dpi=300)
plt.show()
