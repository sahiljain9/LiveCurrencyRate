# Live Exchange Rate Data Pipeline
## Project Overview
A real time data pipeline that fetches live exchange rates for 166 currencies, processes them with 9 feature engineering algorithms, stores data in Azure MySQL, and displays results on a Flask dashboard.

## GitHub Repository
https://github.com/sahiljain9/LiveCurrencyRate

## Live Dashboard
https://dashboard-bpccd3h9fpgmf4bv.switzerlandnorth-01.azurewebsites.net


## Tech Stack
- **Data Source**: open.er-api.com (166 currencies, USD base)
- **Language**: Python 3.12
- **Local DB**: MySQL (XAMPP)
- **Cloud DB**: Azure MySQL Flexible Server
- **Frontend**: Flask + .js
- **Cloud**: Azure Function App (hourly timer trigger)
- **Version Control**: GitHub

## Architecture

1. open.er-api.com - fetches live exchange rates for 166 currencies
2. Azure Function App - triggers pipeline every hour automatically
3. DataFetch and Extract -fetches and structures the raw data
4. SaveFeatures - calculates all 9 features for each currency
5. Azure MySQL - stores all data and features in cloud database
6. Flask Dashboard - queries database and displays results
7. Public URL - accessible from anywhere via Azure Web App

## Feature Engineering Logic

### 1. Volatility
**Formula**: Population Standard Deviation of daily average rates

**Logic**:
- Fetch all available daily average rates from database
- Calculate mean of all daily rates
- Calculate squared difference of each rate from mean
- Take square root of average squared differences
- Higher score = more unstable currency

**Labels**:
- 0.0 = stable (pegged currencies like AED, USD)
- 0.001 - 0.01 = low volatility
- 0.01 - 0.05 = medium volatility
- 0.05+ = high volatility

---

### 2. Anomaly Detection
**Formula**: abs((current - previous) / previous) * 100

**Logic**:
- Fetch last stored rate from database
- Compare with current rate
- Calculate percentage change
- If change > 1% → flag as anomaly

**Labels**:
- 0 = Normal (change <= 1%)
- 1 = Anomaly (change > 1%)

---

### 3. Market Session
**Formula**: UTC hour → session mapping

**Logic**:
- Get current UTC time
- Map to trading session based on market hours
- Asian: 00:00 - 09:00 UTC
- European: 07:00 - 16:00 UTC
- American: 13:00 - 22:00 UTC
- Overlap: 13:00 - 16:00 UTC (Europe + America)
- Off-peak: 22:00 - 00:00 UTC

---

### 4. Price Change
**Formula**: (today - yesterday) / yesterday * 100

**Logic**:
- Fetch yesterday's last rate from database
- Compare with today's current rate
- Calculate percentage change
- Positive = rate increased
- Negative = rate decreased

---

### 5. Prediction (Linear Regression)
**Formula**: y = mx + c (next point on trend line)

**Logic**:
- Fetch last 5 historical rates
- Calculate slope using least squares method
- Extend trend line to predict next rate
- Direction: up/down/stable based on prediction vs current

---

### 6. REER (Real Effective Exchange Rate)
**Formula**: Weighted average of log-normalized rates vs trading partners

**Logic**:
- Compare currency against 9 major trading partners
- Each partner has a weight based on global trade share
- Log normalization handles extreme values (IRR, JPY)
- Score > 110 = overvalued globally
- Score < 90 = undervalued globally
- Score 90-110 = fair value

**Weights**:
- EUR 20%, GBP 15%, JPY 15%, CNY 12%
- CAD 10%, CHF 8%, AUD 8%, INR 7%, KRW 5%

---

### 7. Correlation
**Formula**: Directional agreement score between two currencies

**Logic**:
- Fetch last 5 rates for both currencies
- Calculate daily movement direction (up/down)
- Count how many days both moved in same direction
- Score = matching days / total days
- Score 1.0 = perfect correlation
- Score 0.0 = inverse correlation

**Labels**:
- 0.7+ = high correlation
- 0.4 - 0.7 = medium correlation
- 0.0 - 0.4 = low correlation

---

### 8. Crisis Spread
**Formula**: Percentage volatility per region

**Logic**:
- Group currencies into 5 regions
- Calculate percentage volatility for each currency
- If volatility > 1% → mark as volatile
- Count volatile currencies per region
- More volatile currencies = higher regional risk

**Regions**: Middle East, Europe, Asia, Africa, Americas

**Risk Levels**:
- 0 volatile = low risk
- 1-2 volatile = medium risk
- 3+ volatile = high risk

---

### 9. Currency Converter
**Formula**: amount / from_rate * to_rate

**Logic**:
- All rates are stored as USD base
- Convert amount to USD first
- Then convert from USD to target currency
- Real-time rates from database


## Database Schema
- `raw_rates` — 166 currencies with timestamps
- `currency_features` — All 9 features per currency
- `currency_correlation` — High correlation pairs
- `crisis_spread` — Regional risk levels

## Azure Deployment
- **MySQL**: live-exchange-pipeline.mysql.database.azure.com
- **Function App**: live-exchange-pipeline (hourly timer trigger)
- **Dashboard**: https://dashboard-bpccd3h9fpgmf4bv.switzerlandnorth-01.azurewebsites.net

## How to Run Locally
```bash
pip install flask pymysql requests gunicorn
python Pipeline/SaveFeatures.py
python Pipeline/app.py
```

## Testing
```bash
python Pipeline/Tests/test_volatility.py
python Pipeline/Tests/test_anomaly.py
python Pipeline/Tests/test_market_session.py
python Pipeline/Tests/test_price_change.py
python Pipeline/Tests/test_prediction.py
python Pipeline/Tests/test_reer.py
python Pipeline/Tests/test_correlation.py
python Pipeline/Tests/test_crisis_spread.py
python Pipeline/Tests/test_integration.py
```

## Test Results
- Unit Tests: 20 tests -all passed 
- Integration Tests: 5 tests -all passed 
