# A02 — 5G Architecture & Intelligence

APA-style paper on how 5G is built from software rather than fixed hardware (week of June 15, 2026).

**What I did.** Answered five questions: the difference between the 4G EPC and the 5G Core (dedicated nodes vs. a cloud-native Service-Based Architecture with full control/user-plane separation); why network slicing matters, with real-world examples across the eMBB / URLLC / mMTC service families; what Multi-access Edge Computing (MEC) is and the two ways it cuts latency (shorter path, local breakout); the role of AI in dynamic resource allocation, including the RAN Intelligent Controller in Open RAN; and how the Network Repository Function (NRF) acts as the registry that lets 5G core functions discover each other at run time.

**What I learned.** The headline 4G→5G change is architectural, not radio speed: once network functions are software services on a common bus, slicing, edge placement, and per-function scaling stop being exotic and become normal cloud engineering. The NRF is the keystone — a modular core can only reconfigure itself if its parts can find each other, exactly like service discovery in a microservices platform.

**File.** `ITAI_4370_DEMEL_ASSIGNMENT_2.docx`

**Companion lab.** [L02 — RF Propagation (FSPL)](../../Labs/L02_RF_Propagation_FSPL/) shows the physics behind the architecture: why higher bands force small, dense, edge-heavy cells.
