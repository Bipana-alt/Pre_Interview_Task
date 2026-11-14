# Error-Bounded Lossy Compression of Hurricane ISABEL Pressure Data Using SZ3

## 1. Introduction

Large-scale scientific simulations generate substantial volumes of floating-point data, creating challenges for storage, data movement, and analysis. Error-bounded lossy compression reduces data size while controlling the difference between original and reconstructed values. Unlike lossless compression, it allows a specified amount of reconstruction error in exchange for potentially higher compression ratios.

This study evaluates SZ3 on the Hurricane ISABEL pressure dataset using five relative error bounds ranging from 10⁻² to 10⁻⁶. The objective is to investigate the trade-off between compression ratio, bitrate, and reconstruction quality, measured using peak signal-to-noise ratio (PSNR). Compression and decompression times are also measured, and PSNR is independently verified using Python and NumPy.

## 2. Experimental Methodology

### 2.1 Dataset and Computing Environment

The Hurricane ISABEL pressure field (`Pf48.bin.f32`) contains 25 million single-precision (float32) values with dimensions 100 × 500 × 500. The uncompressed dataset occupies 100,000,000 bytes (100 MB). Its minimum and maximum values are −3411.7407 and 3224.3979, respectively, giving a data range of 6636.1387.

SZ3 was compiled from source on Ubuntu 26.04.1 LTS running through Windows Subsystem for Linux (WSL), using GNU g++ 15.2.0 and CMake 4.2.3. The build completed successfully, and the bundled smoke test passed.

### 2.2 Compression Configuration and Evaluation

Five relative error bounds were evaluated: 10⁻², 10⁻³, 10⁻⁴, 10⁻⁵, and 10⁻⁶. The SZ3 command-line interface was configured for float32 input with dimensions specified as `500 500 100` and relative error mode (`-M REL`).

For each error bound, compression ratio (CR), PSNR, compression time, and decompression time were recorded. Bitrate was calculated as:

**Bitrate = 32 / CR**

The relative error bound ε corresponds to a maximum permitted absolute error of ε × R, where R is the original data range.

PSNR was calculated using:

**PSNR = 20 log₁₀(R) − 10 log₁₀(MSE)**

where MSE is the mean squared error between original and reconstructed values.

Three additional compression/decompression trials were performed for each error bound. Timing results are reported as the mean and sample standard deviation of these three trials.

## 3. Experimental Results

### 3.1 Rate-Distortion Performance

Table 1 summarizes the compression ratio, bitrate, and PSNR for all five error bounds.

**Table 1. SZ3 compression performance on Hurricane ISABEL pressure data.**

| Error bound | Compression ratio | Bitrate (bits/value) | PSNR (dB) |
|---|---:|---:|---:|
| 10⁻² | 939.5582 | 0.0341 | 53.4077 |
| 10⁻³ | 118.0309 | 0.2711 | 69.2793 |
| 10⁻⁴ | 22.1752 | 1.4431 | 86.1715 |
| 10⁻⁵ | 8.4931 | 3.7678 | 104.7712 |
| 10⁻⁶ | 4.9334 | 6.4864 | 125.5756 |

The compression ratio decreased from 939.56 to 4.93 as the relative error bound tightened from 10⁻² to 10⁻⁶. Over the same range, PSNR increased from 53.41 dB to 125.58 dB. This demonstrates that stricter reconstruction accuracy requires a higher bitrate.

The bitrate-versus-PSNR relationship is illustrated in the accompanying rate-distortion figure (`rate_distortion.pdf`).

### 3.2 Compression and Decompression Times

Table 2 presents execution times from three additional trials per error bound.

**Table 2. Execution times in seconds (mean ± sample standard deviation, n = 3).**

| Error bound | Compression time | Decompression time |
|---|---:|---:|
| 10⁻² | 0.3541 ± 0.0501 | 0.1427 ± 0.0027 |
| 10⁻³ | 0.3322 ± 0.0435 | 0.1590 ± 0.0120 |
| 10⁻⁴ | 0.3750 ± 0.0105 | 0.2026 ± 0.0080 |
| 10⁻⁵ | 0.4310 ± 0.0036 | 0.2323 ± 0.0047 |
| 10⁻⁶ | 0.4161 ± 0.0712 | 0.2276 ± 0.0066 |

Decompression was consistently faster than compression. Execution time generally increased as the error bound became stricter, although the trend was not strictly monotonic.

### 3.3 Independent PSNR Verification

PSNR was independently verified for the 10⁻³ error bound using NumPy. Both the original and reconstructed arrays contained 25 million float32 values. Their element-wise differences were used to calculate MSE in float64 precision.

The calculated MSE was 5.1988139989, yielding a PSNR of 69.2792662564 dB. SZ3 reported 69.279266 dB, giving an absolute discrepancy of approximately 2.56 × 10⁻⁷ dB. This is substantially below the required tolerance of 0.001 dB, confirming agreement between the independent calculation and SZ3.

## 4. Discussion

The results demonstrate a clear rate-distortion trade-off. At the loosest error bound (10⁻²), SZ3 achieved a compression ratio of approximately 940, requiring only 0.0341 bits per value on average. However, reconstruction quality was lower, with PSNR of 53.41 dB. At the strictest error bound (10⁻⁶), PSNR increased to 125.58 dB, but the compression ratio decreased to 4.93.

One notable observation was the exceptionally high compression ratio at 10⁻². This suggests that substantial data reduction is possible when relatively large reconstruction errors are permitted. However, whether such an error tolerance is scientifically acceptable depends on the intended application.

Another observation was the variability in compression time. At 10⁻⁶, the three compression trials ranged from 0.3655 to 0.4975 seconds. Possible contributing factors include operating-system scheduling, background activity, and cache effects. The measurements do not establish which factor was responsible.

The experiment has several limitations. Only one scientific field and one compressor were evaluated. The timing experiments were performed under WSL rather than on a dedicated benchmarking system, and only three additional trials were collected per configuration. Furthermore, PSNR and maximum error do not by themselves establish whether the reconstructed data preserves every scientifically important feature.

## 5. Conclusion and Future Work

SZ3 successfully compressed the Hurricane ISABEL pressure dataset at all five tested relative error bounds. Tighter error bounds consistently improved reconstruction quality while reducing compression ratios and increasing bitrate. Independent PSNR verification agreed with SZ3 to within 2.56 × 10⁻⁷ dB, satisfying the required tolerance.

Future work could compare SZ3 with another scientific compressor, such as SZp, evaluate additional scientific fields, and perform more extensive timing measurements under controlled conditions. Application-specific error analysis would also help determine which compression settings preserve the information required for downstream scientific tasks.## 2. Experimental Setup

### 2.1 Dataset and Computing Environment

The experiments used the Hurricane ISABEL pressure field (`Pf48.bin.f32`), consisting of 25 million single-precision (float32) values arranged in a 100 × 500 × 500 array. The original dataset occupied 100 MB (100,000,000 bytes), with values ranging from −3411.7407 to 3224.3979.

SZ3 was compiled from source using GNU g++ 15.2.0 and CMake 4.2.3 on Ubuntu 26.04.1 LTS running under Windows Subsystem for Linux (WSL). The build completed successfully, and the bundled smoke test passed.

### 2.2 Compression Configuration

SZ3 was evaluated using five relative error bounds: 10⁻², 10⁻³, 10⁻⁴, 10⁻⁵, and 10⁻⁶. The input was interpreted as a three-dimensional float32 array, with dimensions supplied to SZ3 as `500 500 100`.

For each error bound, compression ratio, bitrate, PSNR, compression time, and decompression time were recorded. Bitrate was calculated as 32 divided by the compression ratio. The maximum permitted absolute error was determined by multiplying the relative error bound by the original data range.

Compression and decompression were additionally repeated three times per error bound to evaluate timing variability. Mean execution times and sample standard deviations were calculated from these repeated measurements.

### 2.3 Independent PSNR Verification

PSNR was independently calculated for the 10⁻³ error bound using Python and NumPy. The original and reconstructed float32 arrays were compared element by element to calculate mean squared error (MSE). PSNR was then computed using:

PSNR = 20 log₁₀(R) − 10 log₁₀(MSE)

where R represents the range of the original data. The independently calculated result was compared with SZ3's reported PSNR using a tolerance of 0.001 dB.# Error-Bounded Lossy Compression of Hurricane ISABEL Pressure Data Using SZ3

## 1. Introduction

Scientific simulations generate large volumes of floating-point data, making efficient storage and data transfer important challenges. Lossy compression offers a way to reduce data size by allowing small, controlled differences between the original and reconstructed values.

In this experiment, SZ3 was evaluated using the Hurricane ISABEL pressure dataset to investigate the relationship between compression efficiency and reconstruction accuracy. Five relative error bounds, ranging from \(10^{-2}\) to \(10^{-6}\), were tested.

The primary objective was to measure compression ratio, bitrate, peak signal-to-noise ratio (PSNR), and compression and decompression times. PSNR was also independently verified using Python and NumPy to confirm the accuracy of SZ3's reported results.
