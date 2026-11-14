import csv
import statistics
from collections import defaultdict

data = defaultdict(lambda: {"compression": [], "decompression": []})

# Read the recorded timing measurements
with open("timing_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        bound = row["error_bound"]

        data[bound]["compression"].append(
            float(row["compression_seconds"])
        )

        data[bound]["decompression"].append(
            float(row["decompression_seconds"])
        )

# Calculate mean and sample standard deviation
print("Error Bound | Compression (mean ± std) | Decompression (mean ± std)")
print("-" * 75)

for bound in ["1e-2", "1e-3", "1e-4", "1e-5", "1e-6"]:
    comp = data[bound]["compression"]
    decomp = data[bound]["decompression"]

    print(
        f"{bound:11} | "
        f"{statistics.mean(comp):.6f} ± {statistics.stdev(comp):.6f} s | "
        f"{statistics.mean(decomp):.6f} ± {statistics.stdev(decomp):.6f} s"
    )
