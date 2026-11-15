# Error-Bounded Lossy Compression Using SZ3

## 1. Methodology

### 1.1 Environment Setup

I used a Windows computer for this task, so I first set up Windows Subsystem for Linux (WSL) and installed Ubuntu 26.04.1 LTS. I then installed the tools needed to build SZ3, including CMake and a C++ compiler.

I cloned the SZ3 repository from GitHub and built it using CMake in Release mode. My environment used GNU g++ 15.2.0 and CMake 4.2.3. After building SZ3, I ran the provided smoke test to check that it was working correctly. The test passed, and I did not encounter any build errors.

### 1.2 Dataset and Compression Experiments

I downloaded the Hurricane ISABEL pressure dataset and used the file `Pf48.bin.f32`. The dataset contains 25 million float32 values arranged in a 100 × 500 × 500 array, with a total size of 100 MB.

I ran SZ3 on this dataset using five relative error bounds: 10⁻², 10⁻³, 10⁻⁴, 10⁻⁵, and 10⁻⁶. For each error bound, I used the same dataset and recorded the compression ratio, PSNR, compression time, and decompression time.

I calculated the bitrate using:

**Bitrate = 32 / Compression Ratio**

I also repeated the compression and decompression experiments three additional times for each error bound to check the variation in execution times. I calculated the mean and sample standard deviation from these three repeated trials.

### 1.3 PSNR Verification

To check the PSNR reported by SZ3, I wrote a Python script using NumPy. I loaded the original and reconstructed datasets for the 10⁻³ error bound and calculated the mean squared error (MSE).

I then calculated PSNR using the original data range and compared my result with the value reported by SZ3.

My calculated PSNR was 69.2792662564 dB, while SZ3 reported 69.279266 dB. The difference was approximately 2.56 × 10⁻⁷ dB, which is below the required tolerance of 0.001 dB.

## 2. Results

### 2.1 Compression Results

The following table shows the compression ratio, bitrate, and PSNR for the five error bounds.

**Table 1. SZ3 compression results**

| Error bound | Compression ratio | Bitrate (bits/value) | PSNR (dB) |
|---|---:|---:|---:|
| 10⁻² | 939.5582 | 0.0341 | 53.4077 |
| 10⁻³ | 118.0309 | 0.2711 | 69.2793 |
| 10⁻⁴ | 22.1752 | 1.4431 | 86.1715 |
| 10⁻⁵ | 8.4931 | 3.7678 | 104.7712 |
| 10⁻⁶ | 4.9334 | 6.4864 | 125.5756 |

As the error bound became smaller, the compression ratio decreased and PSNR increased. The highest compression ratio was obtained at 10⁻², while the highest PSNR was obtained at 10⁻⁶.

I also created a rate-distortion plot showing bitrate on the x-axis and PSNR on the y-axis. The plot is included separately as `rate_distortion.pdf`.

### 2.2 Compression and Decompression Time

**Table 2. Execution time in seconds (mean ± sample standard deviation, 3 trials)**

| Error bound | Compression time (s) | Decompression time (s) |
|---|---:|---:|
| 10⁻² | 0.3541 ± 0.0501 | 0.1427 ± 0.0027 |
| 10⁻³ | 0.3322 ± 0.0435 | 0.1590 ± 0.0120 |
| 10⁻⁴ | 0.3750 ± 0.0105 | 0.2026 ± 0.0080 |
| 10⁻⁵ | 0.4310 ± 0.0036 | 0.2323 ± 0.0047 |
| 10⁻⁶ | 0.4161 ± 0.0712 | 0.2276 ± 0.0066 |

Decompression was faster than compression for all five error bounds. I also noticed some differences in execution time between repeated runs, even when using the same error bound.

## 3. Discussion

From the results, I observed that there is a trade-off between compression ratio and reconstruction quality. When I used a larger error bound, SZ3 compressed the data much more, but PSNR was lower. When I reduced the error bound, the reconstructed data had a higher PSNR, but the compressed file became larger.

For example, at 10⁻², the compression ratio was approximately 940, while at 10⁻⁶, it was only about 4.93. This shows how much the selected error bound affects the compression results.

I also observed that decompression consistently took less time than compression. The execution times were not exactly the same across repeated runs. Since I performed the experiments using WSL, system activity may have affected the timing measurements, although I did not measure the specific cause of the variation.

## 4. What Surprised Me and Future Work

The most surprising result for me was the very high compression ratio at the 10⁻² error bound. I did not expect the 100 MB dataset to be compressed by such a large factor. However, I also learned that a higher compression ratio does not necessarily mean better results, because the acceptable error depends on how the reconstructed data will be used.

If I had one more week, I would complete the tier 2 and 3 and would also compare SZ3 with SZp with the use of same dataset and error bounds. I would measure both compression quality and throughput to understand which compressor is faster and which provides better compression. I would also repeat the timing experiments more times and test another scientific dataset to see whether the same trends appear.