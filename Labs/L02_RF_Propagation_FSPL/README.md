# L02 — RF Propagation Modeling: Free-Space Path Loss

Python lab modeling how a radio signal weakens with distance and frequency (week of June 15, 2026). Companion to [Assignment 2](../../Assignments/A02_5G_Architecture_and_Intelligence/).

**What I did.** Implemented the ITU free-space path loss model *FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 32.44*. Part 1 runs the course brief's 2.4 GHz scenario over 0.1–20 km. Part 2 extends it to four real-world bands — 900 MHz (low-band), 2.4 GHz (Wi-Fi), 3.5 GHz (5G n78), 28 GHz (mmWave) — and compares the loss at a fixed 1 km.

**Key results.**

| Band | FSPL at 1 km |
|------|-------------:|
| 900 MHz (low-band) | 91.5 dB |
| 2.4 GHz (Wi-Fi) | 100.0 dB |
| 3.5 GHz (5G n78) | 103.3 dB |
| 28 GHz (mmWave) | 121.4 dB |

At 2.4 GHz the loss reaches ~126 dB by 20 km. The 28 GHz band loses ~30 dB more than 900 MHz at the same distance — roughly one-thousandth of the power.

**What I learned.** Both distance and frequency enter the loss logarithmically, so the curves share one shape and just stack by band. That ~30 dB mmWave penalty is the physical reason 5G high-band lives in dense small cells while low-band carries wide-area coverage — network topology is propagation physics made visible.

**Files.** `Lab2_RF_Propagation.ipynb` (submitted notebook), `Lab2_RF_Propagation.pdf`
