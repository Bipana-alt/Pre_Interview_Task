import subprocess
import re
import csv
from pathlib import Path

# SZ3 executable and input data
sz3 = "./build/tools/sz3/sz3"
input_file = "data/Pf48.bin.f32"

# Five error bounds
bounds = ["1e-2", "1e-3", "1e-4", "1e-5", "1e-6"]

# Run each experiment three times
results = []

for bound in bounds:
    for trial in range(1, 4):
        print(f"Running bound={bound}, trial={trial}...", flush=True)

        output_file = f"data/timing_{bound}.f32"

        command = [
            sz3, "-f", "-i", input_file,
            "-o", output_file,
            "-3", "500", "500", "100",
            "-M", "REL", bound, "-a"
        ]

        run = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        output = run.stdout + run.stderr

        compression = re.search(
            r"compression time\s*=\s*([\d.]+)", output
        )
        decompression = re.search(
            r"decompression time\s*=\s*([\d.]+)", output
        )

        if not compression or not decompression:
            raise RuntimeError(f"Could not parse timing:\n{output}")

        results.append([
            bound,
            trial,
            float(compression.group(1)),
            float(decompression.group(1))
        ])

        # Remove temporary reconstructed file to save disk space
        Path(output_file).unlink(missing_ok=True)

# Save measurements
with open("timing_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "error_bound", "trial",
        "compression_seconds", "decompression_seconds"
    ])
    writer.writerows(results)

print("Finished! Results saved to timing_results.csv")
