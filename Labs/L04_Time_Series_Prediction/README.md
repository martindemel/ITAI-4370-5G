# L04 — Time-Series Prediction: ARIMA vs Linear Regression vs LSTM

Three forecasting models compared head-to-head on the same simulated year of hourly network traffic (week of June 29, 2026).

**What I did.** Simulated 8,760 hours of traffic with a daily business-hours cycle, weekday/weekend pattern, yearly trend, seasonal term, noise, and congestion spikes. Explored it (EDA + weekly-period seasonal decomposition), verified stationarity with the Augmented Dickey-Fuller test, and split 80/20 in time order. Then trained and evaluated: **ARIMA(2,1,2)** forecasting the whole test horizon; **Linear Regression** on 16 engineered features (sin/cos encodings of hour, weekday, day-of-year; lags of 1–168 h; moving averages; trend); and a **PyTorch LSTM** (hidden size 32) predicting the next hour from the previous 24.

**Key results.**

| Model | MSE | MAE | RMSE | R² |
|-------|----:|----:|-----:|---:|
| ARIMA(2,1,2) | 2604.37 | 42.38 | 51.03 | −0.181 |
| Linear Regression | 950.83 | 27.42 | 30.84 | 0.572 |
| **LSTM** | **227.12** | **10.68** | **15.07** | **0.897** |

**What I learned.** Match the model to the signal's structure: a non-seasonal ARIMA flattens to the mean of cyclical traffic; hand-built lag features recover the weekly cycle for a linear model; the LSTM learns the daily shape directly from raw sequences and wins. **I found and fixed a target-leakage bug in the brief's feature code** — its moving averages included the hour being predicted, which yields a meaningless R² of 1.0; shifting every window to past-only data makes the scores honest. Fair-comparison caveat stated in the notebook: ARIMA predicts the whole horizon at once while the other two predict one hour ahead, so the gap reflects both model and task.

**Files.** `Lab4_Time_Series_Prediction.ipynb` (submitted notebook), `Lab4_Time_Series_Prediction.pdf`
