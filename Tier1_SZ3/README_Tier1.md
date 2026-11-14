# Tier 1: Error-Bounded Lossy Compression Using SZ3

## 1. Overview

This project evaluates the rate-distortion performance of SZ3 on the Hurricane ISABEL pressure dataset. Five relative error bounds were tested to examine the trade-off between compression ratio, bitrate, reconstruction quality (PSNR), and execution time.

## 2. Computing Environment

- Operating system: Ubuntu 26.04.1 LTS (WSL)
- Compiler: GNU g++ 15.2.0
- CMake: 4.2.3
- Python: Python 3 (virtual environment)
- Python libraries: NumPy 2.5.4 and Matplotlib 3.11.2
- Compressor: SZ3, built from source using CMake

## 3. Dataset

- Dataset: Hurricane ISABEL
- Field: Pressure (`Pf48.bin.f32`)
- Data type: float32
- Dimensions: 100 × 500 × 500
- Total values: 25,000,000
- Original file size: 100,000,000 bytes
- Data range: 6636.138671875

Dataset download:

```bash
mkdir -p data
curl -L -o data/Pf48.bin.f32 https://huggingface.co/datasets/sdrbench/hurricane-isabel/resolve/main/100x500x500/Pf48.bin.f32
```

Verify file size:

```bash
stat -c %s data/Pf48.bin.f32
```

Expected result: `100000000`.

## 4. Build and Smoke Test

From the SZ3 repository directory:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j8
./build/tools/sz3/sz3_smoke_test
```

The smoke test completed successfully with the message `Smoke test passed`.

## 5. Compression Experiments

The five relative error bounds were:

`1e-2`, `1e-3`, `1e-4`, `1e-5`, and `1e-6`.

Commands are executed from the SZ3 repository directory.

```bash
./build/tools/sz3/sz3 -f -i data/Pf48.bin.f32 -o data/decompressed_1e-2.f32 -3 500 500 100 -M REL 1e-2 -a

./build/tools/sz3/sz3 -f -i data/Pf48.bin.f32 -o data/decompressed_1e-3.f32 -3 500 500 100 -M REL 1e-3 -a

./build/tools/sz3/sz3 -f -i data/Pf48.bin.f32 -o data/decompressed_1e-4.f32 -3 500 500 100 -M REL 1e-4 -a

./build/tools/sz3/sz3 -f -i data/Pf48.bin.f32 -o data/decompressed_1e-5.f32 -3 500 500 100 -M REL 1e-5 -a

./build/tools/sz3/sz3 -f -i data/Pf48.bin.f32 -o data/decompressed_1e-6.f32 -3 500 500 100 -M REL 1e-6 -a
```

The `-f` option selects floating-point data, `-3` specifies the three-dimensional array, `-M REL` selects a relative error bound, and `-a` enables reconstruction quality analysis.

## 6. Compression Results

| Error bound | Compression ratio | Bitrate (bits/value) | PSNR (dB) |
|---|---:|---:|---:|
| 1e-2 | 939.558220 | 0.034059 | 53.407718 |
| 1e-3 | 118.030867 | 0.271116 | 69.279266 |
| 1e-4 | 22.175211 | 1.443053 | 86.171536 |
| 1e-5 | 8.493128 | 3.767752 | 104.771242 |
| 1e-6 | 4.933390 | 6.486412 | 125.575613 |

Bitrate was calculated as:

`Bitrate = 32 / compression ratio`

## 7. Independent PSNR Verification

PSNR was independently calculated for the `1e-3` error bound using the original and reconstructed float32 arrays.

Run:

```bash
python verify_psnr.py
```

Results:

- MSE: 5.198813998881138
- Independently calculated PSNR: 69.27926625643147 dB
- SZ3-reported PSNR: 69.279266 dB
- Absolute discrepancy: 2.564314627306885e-7 dB
- Required tolerance: 0.001 dB

The independent verification passed.

## 8. Repeated Timing Measurements

Each error bound was tested three additional times.

Run:

```bash
python repeat_timings.py
python summarize_timings.py
```

Measurements are stored in `timing_results.csv`.

| Error bound | Compression time (s) | Decompression time (s) |
|---|---|---|
| 1e-2 | 0.354061 ± 0.050115 | 0.142663 ± 0.002733 |
| 1e-3 | 0.332228 ± 0.043493 | 0.159023 ± 0.012027 |
| 1e-4 | 0.375000 ± 0.010471 | 0.202603 ± 0.007958 |
| 1e-5 | 0.431020 ± 0.003641 | 0.232298 ± 0.004739 |
| 1e-6 | 0.416125 ± 0.071170 | 0.227605 ± 0.006614 |

Values are reported as mean ± sample standard deviation over three repeated trials.

## 9. Rate-Distortion Plot

Generate the bitrate-versus-PSNR plot using:

```bash
python plot_rate_distortion.py
```

Generated files:

- `rate_distortion.png`
- `rate_distortion.pdf`

## 10. Observations

Tighter error bounds produced higher PSNR and lower compression ratios. Bitrate increased from approximately 0.0341 to 6.4864 bits/value as the relative error bound decreased from `1e-2` to `1e-6`.

Decompression was faster than compression in all repeated experiments. Some timing variability was observed, especially for the `1e-6` compression trials.

These results illustrate the trade-off between compression efficiency and reconstruction accuracy.
