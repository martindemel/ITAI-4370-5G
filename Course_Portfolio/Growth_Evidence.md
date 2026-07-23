# Growth Evidence — From Basic Telecommunications to Advanced AI Applications

This document makes the progression across the course explicit. Every claim links to a dated artifact in this repository, so the trajectory from foundational concepts to advanced applications can be verified, not just asserted.

## Week-by-week trajectory

| Week of | Artifact | Level | Competency demonstrated |
|---------|----------|-------|-------------------------|
| June 8 | [Assignment 1](../Assignments/A01_Telecommunications_Fundamentals/) · [Lab 1](../Labs/L01_Communication_System_Signal_Flow/) | **Foundations** | Telecom vocabulary and the transmitter–channel–receiver model; first working simulation (BPSK over AWGN); validating simulation against closed-form theory |
| June 15 | [Assignment 2](../Assignments/A02_5G_Architecture_and_Intelligence/) · [Lab 2](../Labs/L02_RF_Propagation_FSPL/) | **Physics → Architecture** | Propagation math (FSPL) connected to real deployment decisions; 5G core as cloud-native software (SBA, slicing, MEC, NRF) |
| June 22 | [Assignment 3](../Assignments/A03_AI_ML_and_Open_RAN/) · [Lab 3](../Labs/L03_Network_Traffic_Prediction/) | **First AI application** | Supervised learning applied to a telecom problem: feature engineering, time-ordered evaluation, feature-importance interpretation (test R² 0.893); Open RAN control-plane concepts (RIC, xApps/rApps, SON) |
| June 29 | [Midterm](../Midterm/Network_Simulation_and_Prediction/) · [Lab 4](../Labs/L04_Time_Series_Prediction/) | **Advanced modeling** | Three simulation/AI paradigms (discrete-event, agent-based, predictive); three forecasting families compared (ARIMA / regression / **PyTorch LSTM**, R² 0.897); independent discovery and fix of a target-leakage bug |
| July 6 | [Lab 5](../Labs/L05_Edge_Model_Optimization/) | **Advanced deployment** | Neural-network compression built by hand (pruning, INT8 quantization, knowledge distillation, 10.5×); full reimplementation of a TensorFlow brief in PyTorch |
| July 13+ | [Final Exam Portfolio](../Final_Exam_Portfolio/) · [Course Portfolio](./) | **Synthesis** | Module-by-module integration of physics, architecture, and intelligence; reflective analysis of the learning arc |
| July 20 | [Assignment 4](../Assignments/A04_Ethical_AI/) | **Responsible AI** | Ethics of AI systems: international frameworks (IEEE, UNESCO, OECD, EU AI Act), scenario analysis, and accountability for the autonomous networks built earlier in the course |

## Skills matrix: where I started → where I ended

| Skill area | Start of course | End of course — evidence |
|------------|-----------------|--------------------------|
| Signal processing | None — telecom was a black box | Built and validated a BPSK link end-to-end; Monte-Carlo BER matching ½·erfc(√(E<sub>b</sub>/N<sub>0</sub>)) to within a few percent ([Lab 1](../Labs/L01_Communication_System_Signal_Flow/)) |
| RF engineering | Could not read a link budget | Computed and interpreted FSPL across four bands; explained mmWave small-cell economics from a 30 dB delta ([Lab 2](../Labs/L02_RF_Propagation_FSPL/)) |
| Machine learning | General awareness | Engineered features, trained and honestly evaluated Random Forests, linear models, and an LSTM; read feature importances as domain insight ([Lab 3](../Labs/L03_Network_Traffic_Prediction/), [Lab 4](../Labs/L04_Time_Series_Prediction/)) |
| Deep learning | Had not written a neural network | LSTM forecaster + three compression techniques implemented at tensor level in PyTorch ([Lab 4](../Labs/L04_Time_Series_Prediction/), [Lab 5](../Labs/L05_Edge_Model_Optimization/)) |
| Evaluation rigor | Trusted reported metrics | Time-ordered splits; caught and fixed target leakage (R² 1.0 → honest 0.572); documented fair-comparison caveats ([Lab 4](../Labs/L04_Time_Series_Prediction/)) |
| Network simulation | None | Discrete-event (SimPy) and agent-based (Mesa) models of latency, congestion, and self-healing ([Midterm](../Midterm/Network_Simulation_and_Prediction/)) |
| 5G/O-RAN architecture | Buzzword level | Can explain EPC vs 5GC, SBA/NRF, slicing service classes, MEC placement, Near-RT vs Non-RT RIC with concrete examples ([A02](../Assignments/A02_5G_Architecture_and_Intelligence/), [A03](../Assignments/A03_AI_ML_and_Open_RAN/)) |
| Technical communication | Operational documentation (ITSM) | Four APA papers, six reproducible notebooks, and this structured public portfolio |

## Three progression arcs (with proof)

**1. From running code to correcting it.** The clearest growth signal in this portfolio is how my relationship to the provided lab code changed. Week 1: I ran the course's BPSK example and extended it ([Practical-example lineage in Lab 1](../Labs/L01_Communication_System_Signal_Flow/)). Week 3: I added engineered features and honest splits to a provided scaffold ([Lab 3](../Labs/L03_Network_Traffic_Prediction/)). Week 4: I **found a bug in the brief itself** — moving-average features that leaked the prediction target — and fixed it ([Lab 4, Part 5](../Labs/L04_Time_Series_Prediction/)). Week 5: when the brief's TensorFlow stack crashed, I **reimplemented the entire lab in PyTorch**, including a distillation loss the brief defined but never used ([Lab 5](../Labs/L05_Edge_Model_Optimization/)). That is a progression from consumer of course material to critical contributor.

**2. From bits to intelligence.** The artifacts trace the course's conceptual ladder rung by rung: individual bits on a carrier (Lab 1) → power over distance (Lab 2) → traffic as a learnable signal (Lab 3) → competing forecasting architectures (Lab 4) → intelligence compressed to fit the network edge (Lab 5). Each artifact consumes the previous one's concepts: the BER curve motivates SNR-aware design, path loss motivates edge placement, prediction motivates the RIC, and compression makes edge prediction deployable.

**3. From single metrics to judgment.** Early work reports one number (0 bit errors). Mid-course work reports metric families (MSE/MAE/RMSE/R²). Late work reports **trade-off spaces** — accuracy vs size vs latency vs compression across four model variants — plus the caveats that keep the numbers honest. Reporting maturity is skill maturity.

## Performance summary (assessment artifacts)

All graded artifacts are in this repository as evidence of performance and progress: [four assignments](../Assignments/), [five laboratories](../Labs/) (each notebook with embedded, reproducible results), the [midterm](../Midterm/Network_Simulation_and_Prediction/), and the [Final Exam portfolio](../Final_Exam_Portfolio/) (17-page PDF). Headline results: BER validated to theory (Lab 1), FSPL band analysis (Lab 2), test R² 0.893 (Lab 3), LSTM R² 0.897 beating ARIMA and regression (Lab 4), 10.5× model compression at −3.5 accuracy points (Lab 5).
