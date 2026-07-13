# Midterm — Network Simulation & Predictive Optimization

Three hands-on problems combining discrete-event simulation, agent-based modeling, and machine learning — three complementary ways to study a network before touching real hardware.

**What I did.**

1. **Network traffic simulation (SimPy).** A discrete-event simulation of packets flowing through a chain of three routers. Each packet requests each router in turn (capacity 1, fixed 2-time-unit processing delay), so the simulation exposes queueing: the printed trace shows per-packet generation, per-hop processing, and total end-to-end delay for 10 packets.
2. **Agent-based network modeling (Mesa).** Five router agents placed on a Watts–Strogatz small-world graph (k = 3, p = 0.5). Each step, every router's load drifts randomly (±10, clamped to 0–100); any router crossing the 80% threshold announces overload and reroutes traffic. Ten steps of the model show congestion appearing and dissipating from purely local rules.
3. **Predictive optimization (scikit-learn).** A linear-regression traffic predictor on synthetic sinusoidal traffic with noise, using the previous observation (lag-1) as the feature. Trained on an 80/20 split, scored with mean squared error, and plotted actual vs. predicted load — the AI step that turns simulation into self-optimization.

**What I learned.** Discrete-event simulation captures *when* things happen — queueing and cumulative latency fall out of the event calendar for free. Agent-based modeling captures *emergence* — congestion and recovery arise from local per-router rules with no central controller, which is exactly the philosophy behind Self-Organizing Networks. And a simple lagged regression is enough to close the loop from *observing* traffic to *anticipating* it, which is the seed of every intelligent-RAN application in this course.

**File.** `Mid Term.txt` — the three solutions as submitted (SimPy, Mesa, and scikit-learn sections separated by comment dividers).
