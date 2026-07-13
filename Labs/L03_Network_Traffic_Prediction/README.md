# L03 — Network Traffic Prediction (Supervised Learning)

Machine-learning lab predicting hourly network traffic from its own history (week of June 22, 2026). Companion to [Assignment 3](../../Assignments/A03_AI_ML_and_Open_RAN/).

**What I did.** Generated a synthetic year of hourly telecom traffic with daily, weekly, annual, and business-hours patterns plus noise; engineered lag features (1 h and 24 h back) and a 7-day rolling average; trained a 100-tree Random Forest regressor; and evaluated it on a strictly time-ordered 80/20 split so the model is scored only on later hours it has never seen — the same setup as real forecasting.

**Key results.**

| Metric | Train | Test |
|--------|------:|-----:|
| MSE | 17.58 | 34.65 |
| R² | 0.946 | **0.893** |

Feature importance: `traffic_lag_1h` 0.816 · `hour` 0.078 · `traffic_lag_24h` 0.036 — recent history and time of day carry almost all the signal.

**What I learned.** Traffic is habitual, so the previous hour is by far the strongest predictor. Forecasting evaluation must respect time order — shuffling leaks the future into training. This one-hour-ahead prediction is precisely what an Open RAN xApp consumes to allocate physical resource blocks before congestion forms.

**Files.** `Lab3_Traffic_Prediction.ipynb` (submitted notebook), `Lab3_Traffic_Prediction.pdf`
