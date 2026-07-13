# A03 — AI/ML Applications & Open RAN

APA-style paper on where machine learning actually runs inside a modern radio access network (week of June 22, 2026).

**What I did.** Answered five questions: an AI/ML example for radio resource management (predictive resource-block scheduling via an xApp) and one for reliability (anomaly detection ahead of faults); how Self-Organizing Networks self-optimize (tilt, power, handover, load balancing) and self-heal (neighbors cover a failed cell), and how predictive maintenance protects Quality of Service; what normalizing user demand achieves in a resource-allocation simulation and how it maps to proportional scheduling of physical resource blocks; two key differences between traditional RAN and Open RAN (single-vendor integration vs. RU/DU/CU disaggregation, proprietary vs. open standardized interfaces); and the division of labor between the Near-RT RIC (10 ms–1 s loops, xApps) and Non-RT RIC (>1 s loops, rApps, policies and model training).

**What I learned.** The RAN runs on two clocks: the Non-RT RIC plans and learns, the Near-RT RIC acts. Open interfaces are the economic story — once the connection points are public, operators can mix vendors and small suppliers can compete. Normalization is the quiet workhorse: proportional shares are what make a fixed radio resource pool fair, comparable, and numerically stable.

**File.** `ITAI_4370_DEMEL_ASSIGNMENT_3.docx`

**Companion lab.** [L03 — Network Traffic Prediction](../../Labs/L03_Network_Traffic_Prediction/) builds exactly the kind of demand forecast these controllers consume.
