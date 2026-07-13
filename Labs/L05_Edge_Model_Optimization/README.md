# L05 — Edge Computing Simulation: Model Optimization

Compressing a neural network until it fits on an edge device — and measuring exactly what that costs (week of July 6, 2026).

**What I did.** Trained a baseline "cloud" MLP (128→64→32) to classify device states from synthetic IoT sensor data (10,000 samples, 20 features, 3 classes), then applied three compression techniques: **pruning** (L1-unstructured removal of the smallest 50% of weights, followed by fine-tuning), **INT8 quantization** (symmetric per-layer weight quantization), and **knowledge distillation** (a 10× smaller student trained on the teacher's temperature-softened logits, T = 3, α = 0.5). Measured accuracy, storage size, parameter count, and median inference latency for each, and mapped each technique to the device class it suits. The brief targeted TensorFlow/TFLite, which crashed in my environment, so I reimplemented the whole lab in PyTorch — making each technique real, including the distillation loss the brief defined but never used.

**Key results.**

| Model | Accuracy | Size (KB) | Params | Inference (ms) | Compression |
|-------|---------:|----------:|-------:|---------------:|------------:|
| Baseline (cloud) | 96.2% | 51.26 | 13,123 | 0.053 | 1.0× |
| Pruned (50%) | 96.7% | 26.07 | 13,123 (49.1% zero) | 0.054 | 2.0× |
| Quantized (INT8) | 96.1% | 12.82 | 13,123 | 0.055 | 4.0× |
| Distilled | 92.7% | 4.89 | 1,251 | **0.029** | **10.5×** |

Deployment mapping: distilled/INT8 → microcontrollers · pruned/quantized → edge gateways · full baseline → edge servers.

**What I learned.** Compression is a trade-off space: pruning and quantization keep accuracy at 2–4× smaller storage, distillation buys 10× and the fastest inference for ~3.5 accuracy points. Only the genuinely smaller architecture ran faster on standard hardware — zeroed weights and simulated INT8 shrink storage but need sparse/integer execution units to speed up compute. This is the enabling step for the MEC low-latency story from Assignment 2.

**Files.** `Lab5_Edge_Model_Optimization.ipynb` (submitted notebook), `Lab5_Edge_Model_Optimization.pdf`
