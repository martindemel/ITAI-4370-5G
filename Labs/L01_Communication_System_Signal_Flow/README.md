# L01 — Communication System & Signal Flow (BPSK over AWGN)

Hands-on lab modeling a digital communication system as a block diagram and as a working Python simulation (week of June 8, 2026). Companion to [Assignment 1](../../Assignments/A01_Telecommunications_Fundamentals/).

**What I did.** Part 1: drew the five-block chain `Source → Modulator → Channel → Demodulator → Receiver` in Draw.io and reproduced it programmatically in Matplotlib, with the AWGN noise source feeding the channel. Part 2: simulated the full chain in NumPy — random bits mapped to BPSK symbols (0 → −1, 1 → +1) on a cosine carrier, Gaussian noise added in the channel, coherent demodulation (multiply by carrier, integrate-and-dump), threshold detection. The extended notebook and analysis suite add received constellations at two SNRs and a 1,000,000-bit-per-point Monte-Carlo BER sweep validated against theory.

**Key results.**
- Perfect recovery of the transmitted bits at σ = 0.5 (zero errors).
- Simulated BER matches ½·erfc(√(E<sub>b</sub>/N<sub>0</sub>)) across 0–10 dB (at 7 dB: 7.78e-4 simulated vs 7.73e-4 theory).
- The constellation clouds visibly tighten as SNR rises; every sample crossing I = 0 is a bit error.

**What I learned.** BPSK is just 180° phase flips; the channel is the only place the signal degrades; and coherent demodulation with integrate-and-dump is the matched filter — optimal for BPSK in AWGN. A simulation is validated when it reproduces theory, not when it merely runs.

## Files

| File | Description |
|------|-------------|
| `Lab1_Communication_System.ipynb` | Submitted notebook (markdown + code + outputs) |
| `Lab1_Communication_System.pdf` | Submitted notebook as PDF |
| `DEMEL_LABORATORY_1.drawio.png` | Submitted Draw.io block diagram |
| `extended/Lab1_Communication_System_detailed.ipynb` | Extended version: constellation + Monte-Carlo BER vs theory |
| `extended/diagrams/` | Editable `.drawio` + rendered block diagram (PNG/SVG) |
| `extended/figures/` | Signal flow, constellation, BER curve figures |
| `analysis/bpsk_comm_analysis.py` | Standalone BPSK analysis suite that regenerates every figure |
| `analysis/*.png/svg/drawio` | Its outputs: block diagram, signal flow, constellation, BER curve |
