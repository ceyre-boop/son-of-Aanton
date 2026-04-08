# The Intelligence System MOC 🧠

#data #statistics #machine-learning #institutional #hedge-funds #multi-asset #prediction #causation #differential-equations

> Core Philosophy: You cannot match institutional speed. You don't need to. They leave footprints in mandated filings, correlated markets, and order flow. Statistics finds the footprints. Math models where they lead. Time and trials build certainty.

---

## 🗺 Map of Contents

- [[#Part 1 — Free Data Sources (The Full Stack)]]
- [[#Part 2 — Institutional Intelligence (Reading the Giants)]]
- [[#Part 3 — Mandated Filings as Alpha]]
- [[#Part 4 — The Prediction Architecture]]
- [[#Part 5 — Multi-Asset Correlation Engine]]
- [[#Part 6 — Causation vs Correlation vs Confounding]]
- [[#Part 7 — The Mathematics of Prediction]]
- [[#Part 8 — Differential Equations in Markets]]
- [[#Part 9 — Proper Statistical Sampling & Significance]]
- [[#Part 10 — Building the Full System (Son of Anton Integration)]]
- [[#Part 11 — The Analysis File Structure]]

---

## Part 1 — Free Data Sources (The Full Stack)

> You need price data, fundamentals, macro, filings, sentiment, and alternative. All of it is available free or near-free. Here is every source worth knowing.

### Tier 1 — Completely Free, Production-Quality

| Source | Data | Python Access | Rate Limit |
|--------|------|---------------|------------|
| **yfinance** | OHLCV, dividends, splits, fundamentals | `yfinance.Ticker("AAPL").history()` | None |
| **FRED API** | 800K+ macro series (Fed, Treasury, BLS) | `fredapi.Fred(api_key).get_series('GDP')` | 120/min |
| **BLS API** | Employment, wages, inflation direct | `requests.get(bls_url)` | 500/day |
| **EIA API** | Energy production, consumption, storage | `eia-python` package | 1M calls/month |
| **USDA API** | Crop reports, inventory, planting | `requests.get(usda_url)` | High |
| **CBOE Datashop** | VIX, options chains, skew | `pandas.read_csv(cboe_url)` | None |
| **CFTC COT Reports** | Institutional futures positioning | `pandas.read_excel(cftc_url)` | Weekly |
| **SEC EDGAR** | 13F, 13D, Form 4 filings | `sec-edgar-downloader` | 10 req/s |
| **Alpha Vantage** | 15+ years OHLCV, indicators | `alphavantage-api` | 5/min (free) |
| **IEX Cloud** | Real-time quotes, fundamentals | `iexfinance` | 50K msgs/month |

### Tier 2 — Free with Registration

| Source | Unique Data | Access |
|--------|-------------|--------|
| **Quandl/NASDAQ Data Link** | Futures, options, sentiment | `quandl.get("WIKI/AAPL")` |
| **St. Louis Fed (FRED)** | Economic indicators, yield curves | Direct CSV/API |
| **Yahoo Finance Premium** | Historical constituents | `yfinance` (unofficial) |
| **Reddit API** | Sentiment, trending tickers | `PRAW` |
| **Twitter/X API** | Social sentiment, news velocity | `tweepy` (v2) |

### Tier 3 — Dark Pool & Alternative (Proxies)

```python
# Dark Pool Volume (proxy via FINRA)
# No direct API, but available via:
# 1. Cboe Global Indices (VIX related)
# 2. FINRA ADF data (delayed)
# 3. Proxy: High volume outside NBW = dark pool

# Options Flow (proxy)
# CBOE VVIX (VIX of VIX) = options market stress
# Put/Call ratio = sentiment
# Unusual volume = institutional positioning
```

---

## Part 2 — Institutional Intelligence (Reading the Giants)

> Hedge funds and institutions are mandated by law to disclose. The filings are public. The alpha is in reading them faster and smarter than the market.

### The Disclosure Mandate

| Entity | Must File | What They Reveal |
|--------|-----------|------------------|
| **Institutional Investors** | 13F quarterly | All equity holdings >$100M |
| **Corporate Insiders** | Form 4 within 2 days | Every buy/sell of own stock |
| **Activist Investors** | 13D within 10 days | Intent to influence management |
| **Investment Managers** | ADV annually | Strategy, AUM, conflicts |
| **Private Funds** | Form PF quarterly | Risk metrics, leverage, exposure |

### The 13F Intelligence

```python
# What 13F tells you:
# - Exact holdings of every major fund (Buffett, Druckenmiller, Soros)
# - Position changes (added, reduced, eliminated)
# - Concentration (how concentrated is their book?)
# - Turnover (are they trading or holding?)

# Lag: 45 days after quarter-end
# Use: Confirm trends, find crowded trades, spot accumulation

# Python access:
from sec_edgar_downloader import Downloader
dl = Downloader("MyCompany", "my@email.com")
dl.download("13F-HR", "0001067983")  # Berkshire Hathaway CIK

# Parse with pandas
import pandas as pd
df = pd.read_xml("path/to/13f.xml")
```

### Form 4: The Real-Time Signal

```python
# Form 4 = Insider transactions
# Filed within 2 business days
# Most real-time institutional signal available

# Signal quality:
# - CEO/CFO buys = high conviction (rare, powerful)
# - Cluster buying (multiple insiders) = very bullish
# - Selling after rally = profit taking (neutral)
# - Selling into decline = concerning

# SEC EDGAR RSS feed for real-time:
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4
```

---

## Part 3 — Mandated Filings as Alpha

### 13D: The Activist Warning System

```python
# 13D = Investor owns >5% and intends to influence
# Filed within 10 days of crossing 5%
# Must disclose: Purpose, plans, source of funds

# Why it matters:
# - Carl Icahn files 13D → stock usually pops
# - Activist intent = forced change (management shakeup, spinoffs)
# - The 10-day window = information asymmetry opportunity

# Watch for:
# - "Shareholder engagement" = nice words for proxy fight
# - "Strategic alternatives" = sell the company
# - "Board representation" = seats on board
```

### Earnings Transcript NLP

```python
# Q/A section > Prepared remarks
# Analyst pushback = red flag
# Management deflection = bigger red flag
# "Challenging environment" = things are bad
# "Robust pipeline" = nothing concrete to say

# NLP signals:
# - Sentiment score change QoQ
# - Uncertainty words ("may", "might", "could")
# - Guidance specificity (numbers vs vague)
# - Analyst tone (aggressive vs supportive)

# Free source: Seeking Alpha transcripts (delayed)
# Fast source: FactSet/Bloomberg (expensive)
```

---

## Part 4 — The Prediction Architecture

> Four layers of prediction, each operating at different timescales. Ensembled together.

### The Four Layers

| Layer | Timescale | Methods | Data |
|-------|-----------|---------|------|
| **Structural** | Months-years | Demographics, debt cycles, regime change | FRED, BIS, IMF |
| **Fundamental** | Weeks-months | Earnings, guidance, competitive position | EDGAR, transcripts |
| **Macro-Regime** | Days-weeks | Fed policy, yield curve, credit spreads | FRED, CME FedWatch |
| **Technical-ICT** | Hours-days | Order flow, liquidity, market structure | CBOE, on-chain |

### Ensemble Scoring Function

```python
def ensemble_prediction(
    structural_score: float,  # -1 to 1
    fundamental_score: float, # -1 to 1
    macro_score: float,       # -1 to 1
    technical_score: float,   # -1 to 1
    
    # Weights (sum to 1.0)
    w_structural: float = 0.15,
    w_fundamental: float = 0.25,
    w_macro: float = 0.30,
    w_technical: float = 0.30
) -> dict:
    """
    Combine four layers into single prediction.
    Weights reflect confidence in each layer's predictive power.
    """
    
    # Base ensemble
    ensemble = (
        structural_score * w_structural +
        fundamental_score * w_fundamental +
        macro_score * w_macro +
        technical_score * w_technical
    )
    
    # Confidence based on agreement
    scores = [structural_score, fundamental_score, macro_score, technical_score]
    agreement = 1 - (np.std(scores) / 2)  # 1 = perfect agreement, 0 = max disagreement
    
    # Boost confidence if all agree
    if all(s > 0 for s in scores) or all(s < 0 for s in scores):
        confidence = min(0.95, 0.6 + agreement * 0.35)
    else:
        confidence = 0.5 + agreement * 0.2
    
    return {
        "direction": "LONG" if ensemble > 0 else "SHORT",
        "magnitude": abs(ensemble),
        "confidence": confidence,
        "agreement": agreement,
        "layer_breakdown": {
            "structural": structural_score,
            "fundamental": fundamental_score,
            "macro": macro_score,
            "technical": technical_score
        }
    }
```

---

## Part 5 — Multi-Asset Correlation Engine

> Oil doesn't move in isolation. It ripples through ethanol to corn, through shipping costs to retail, through inflation expectations to bonds.

### The Inter-Market Chain

```
Oil (CL) 
  → Gasoline (RB) → Transportation costs
  → Ethanol (corn) → Food prices
  → Plastics (chemicals) → Manufacturing
  → Shipping (Baltic Dry) → Global trade
  → Inflation (CPI) → Fed policy
  → Bonds (TLT) → Equity discount rates
  → Stocks (SPY) → Your position
```

### Rate Chain

```
Fed Funds → 2Y Treasury → 10Y Treasury → 30Y Treasury
                ↓              ↓                ↓
          Bank lending    Mortgage rates   Pension liabilities
                ↓              ↓                ↓
          Credit cards     Housing market    Duration risk
```

### Risk Chain

```
VIX (equity vol) → VVIX (vol of vol) → Credit spreads (HYG)
      ↓                     ↓                   ↓
   Fear gauge          Options stress      Default probability
      ↓                     ↓                   ↓
   Risk-off flows    Gamma positioning    Flight to safety
```

### Correlation vs Causation

```python
# Oil and stocks are NEGATIVELY correlated in supply shocks
# Oil and stocks are POSITIVELY correlated in demand booms

# Same two assets, opposite correlations depending on regime.
# The correlation tells you nothing without knowing the regime.

# Regime identification:
# - Rising oil + rising yields + falling stocks = supply shock (stagflation)
# - Rising oil + rising stocks + flat yields = demand boom (growth)
```

---

## Part 6 — Causation vs Correlation vs Confounding

### The Three-Variable Problem

```python
# X and Y correlate. Three possibilities:
# 1. X → Y (causation)
# 2. Y → X (reverse causation)
# 3. Z → X and Z → Y (confounding)

# Example: Ice cream sales and drowning deaths correlate
# X: Ice cream sales
# Y: Drowning deaths
# Z: Temperature (confounder)
```

### Granger Causality Test

```python
from statsmodels.tsa.stattools import grangercausalitytests

# Tests if X helps predict Y
# Not true causation, but predictive causation

# Does oil predict corn prices?
data = pd.DataFrame({'oil': oil_prices, 'corn': corn_prices})
result = grangercausalitytests(data[['oil', 'corn']], maxlag=5)

# If p < 0.05, oil "Granger-causes" corn
# Meaning: past oil prices contain information about future corn prices
```

### Partial Correlation

```python
# Correlation between X and Y, controlling for Z
from scipy.stats import pearsonr

# Correlation between oil and corn
# CONTROLLING for ethanol prices (since ethanol links them)

from pingouin import partial_corr
result = partial_corr(data=df, x='oil', y='corn', covar='ethanol')

# If partial correlation drops to near zero:
# Oil and corn weren't directly related, only through ethanol
```

### Cointegration

```python
# Two series wander, but their DIFFERENCE is stationary
# Classic pairs trading signal

from statsmodels.tsa.stattools import coint

score, p_value, _ = coint(asset_a, asset_b)

# If p < 0.05: cointegrated
# Meaning: they diverge, but always mean-revert to each other
# Trade: Long the underperformer, short the outperformer
```

---

## Part 7 — The Mathematics of Prediction

### Information Theory

```python
# Mutual Information: How much does X tell you about Y?
from sklearn.feature_selection import mutual_info_regression

mi = mutual_info_regression(X_features, y_returns)
# Higher MI = better predictive feature

# Entropy: Uncertainty in the distribution
from scipy.stats import entropy

price_entropy = entropy(histogram_of_returns)
# Higher entropy = more randomness = harder to predict
```

### Bayesian Updating

```python
# Start with prior belief, update with evidence

# Prior: 60% win rate based on backtest
# Evidence: 3 losses in a row
# Posterior: Updated win rate

def bayesian_update(prior_win_rate, n_recent, n_wins):
    """
    Update win rate belief with recent evidence
    """
    prior_alpha = prior_win_rate * 100  # pseudo-counts
    prior_beta = (1 - prior_win_rate) * 100
    
    posterior_alpha = prior_alpha + n_wins
    posterior_beta = prior_beta + (n_recent - n_wins)
    
    posterior_win_rate = posterior_alpha / (posterior_alpha + posterior_beta)
    
    return posterior_win_rate

# After 3 losses, 60% prior → ~58% posterior
# Evidence slightly downgraded confidence
```

---

## Part 8 — Differential Equations in Markets

### Ornstein-Uhlenbeck (Mean Reversion)

```python
# dX = θ(μ - X)dt + σdW

# X = current price
# μ = long-term mean
# θ = speed of reversion
# σ = volatility
# dW = Wiener process (random noise)

# Half-life of mean reversion:
# t_half = ln(2) / θ

# Trading application:
# - Measure half-life of pairs
# - Enter when deviation > 2 std
# - Exit at half-life or mean

import numpy as np

def estimate_ou_params(prices):
    """Estimate OU parameters from price series"""
    log_prices = np.log(prices)
    
    # Fit AR(1) model
    from statsmodels.tsa.ar_model import AutoReg
    model = AutoReg(log_prices, lags=1).fit()
    
    phi = model.params[1]  # AR(1) coefficient
    theta = -np.log(phi)
    half_life = np.log(2) / theta
    
    return theta, half_life
```

### Logistic Growth (Market Cycles)

```python
# dP/dt = rP(1 - P/K)

# P = price/adoption
# r = growth rate
# K = carrying capacity (max price)

# S-curve phases:
# 1. Slow growth (accumulation)
# 2. Exponential growth (mania)
# 3. Deceleration (distribution)
# 4. Plateau (new equilibrium)

# Trading: Identify which phase, position accordingly
```

### Coupled ODEs (Macro System)

```python
# The economy as a system of differential equations:

# d(Unemployment)/dt = f(GDP growth, interest rates)
# d(Inflation)/dt = g(money supply, velocity, unemployment)
# d(Asset prices)/dt = h(discount rates, earnings growth, risk premium)

# No closed-form solution.
# Numerical integration with real data.
# Predicts regime transitions before they appear in prices.
```

---

## Part 9 — Proper Statistical Sampling & Significance

### How Many Trades Do You Actually Need?

```python
# For Sharpe ratio precision:
# SE(Sharpe) ≈ 1/sqrt(N)
# For 95% CI of ±0.5 around Sharpe 1.0:
# N = (2/0.5)^2 = 16

# For strategy comparison (Sharpe 1.0 vs 1.2):
# Need ~600 trades for 80% power at 5% significance

# Rule of thumb:
# - Minimum: 100 trades (barely valid)
# - Comfortable: 300-500 trades
# - Robust: 1000+ trades
```

### Multiple Testing Problem

```python
# Test 100 strategies, 5 will look significant by chance (p < 0.05)
# Bonferroni correction: alpha / n_tests
# For 100 strategies: need p < 0.0005 for significance

from statsmodels.stats.multitest import multipletests

p_values = [test_strategy(s) for s in strategies]
rejected, p_corrected, _, _ = multipletests(p_values, method='fdr_bh')
# FDR = False Discovery Rate (Benjamini-Hochberg)
# Less conservative than Bonferroni
```

### Walk-Forward Validation

```python
# The only valid backtest method:

# 1. Train on 2000-2010
# 2. Validate on 2010-2015
# 3. Retrain on 2000-2015
# 4. Validate on 2015-2020
# 5. Continue rolling...

# Never optimize on test data.
# If Sharpe drops from 2.0 (train) to 0.5 (test), it's overfit.

from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    # Score should be consistent across folds
```

---

## Part 10 — Building the Full System (Son of Anton Integration)

### The Architecture

```
[Data Layer]          [Analysis Layer]         [Decision Layer]
yfinance                Feature Engineering      XGBoost ensemble
FRED                    Regime Classification    Kimi escalation
EDGAR                   Causality Testing        Risk sizing
COT                     ODE Integration          Game theory

→ All feed into →    [Son of Anton Core]      → Trade execution
```

### Ollama Prompts for Son of Anton

```python
# Prompt 1: Earnings Transcript Analysis
TRANSCRIPT_PROMPT = """
You are a forensic accountant analyzing an earnings call.

Read this transcript section and identify:
1. Guidance specificity (numbers vs vague words)
2. Analyst pushback (aggressive questions)
3. Management deflection (avoiding answers)
4. Tone shift from previous quarter

Rate BULLISH/NEUTRAL/BEARISH with confidence 0-1.
Explain reasoning in one sentence.

Transcript: {transcript}
"""

# Prompt 2: COT Report Interpretation
COT_PROMPT = """
You are a CFTC Commitment of Traders analyst.

Given this week's COT data:
- Commercial hedgers: {commercial_net} net position
- Large speculators: {spec_net} net position
- Small speculators: {small_net} net position

Commercials are SMART MONEY (producers/users).
Speculators are DUMB MONEY (trend chasers).

Interpret: What is smart money doing? What is dumb money doing?
Rate BULLISH/NEUTRAL/BEARISH for next 4 weeks.
"""

# Prompt 3: Daily Brief Generation
BRIEF_PROMPT = """
You are Son of Anton, an AI trading system.

Current state:
- Portfolio: {positions}
- Signals today: {signals}
- Macro regime: {regime}

Write a 3-sentence brief:
1. What happened today
2. What signals are active
3. What to watch tomorrow

Be concise. Use trading terminology.
"""
```

### The Full Loop

```python
# 06:00 UTC: Data ingestion
fetch_overnight_data()
update_macro_dashboard()

# 06:30 UTC: Feature generation
build_features(all_assets)
classify_regimes()

# 07:00 UTC: Signal generation
xgboost_signals = generate_signals_xgboost()
for signal in xgboost_signals:
    if 0.5 <= signal.confidence <= 0.7:
        kimi_analysis = escalate_to_kimi(signal)
        signal = ensemble_decision(signal, kimi_analysis)

# 07:30 UTC: Risk and sizing
for signal in confirmed_signals:
    risk = calculate_kelly_sizing(signal)
    game = game_theory_validation(signal)
    if game.nash_equilibrium_favorable:
        stage_trade(signal, risk)

# 08:00 UTC: Execution
for staged_trade in staged:
    if all_gates_pass(staged_trade):
        execute_with_slippage_model(staged_trade)

# Continuous: Learning
trade_outcomes = monitor_positions()
update_bayesian_win_rates(trade_outcomes)
retrain_xgboost_if_sample_size_sufficient()
```

---

## Part 11 — The Analysis File Structure

```
vault/
├── intelligence/
│   ├── MOC.md                    # This file
│   ├── sources/                  # Data source configs
│   │   ├── fred_series.yml
│   │   ├── sec_filings.yml
│   │   └── cot_symbols.yml
│   ├── models/                   # Trained models
│   │   ├── xgboost_bias_v1.pkl
│   │   ├── regime_classifier.pkl
│   │   └── ou_half_life.json
│   ├── signals/                  # Generated signals
│   │   ├── 2024-01-15_signals.json
│   │   └── latest_signals.json
│   └── research/                 # Active research
│       ├── oil_corn_causation.md
│       ├── ou_pairs_analysis.md
│       └── regime_transition_math.md
├── trades/
│   ├── journal/                  # Trade journal
│   ├── backtests/                # Backtest results
│   └── performance/              # Performance attribution
└── system/
    ├── prompts/                  # Ollama prompts
    ├── config.yml                # System config
    └── state.json                # Current state
```

---

> "The market is a device for transferring money from the impatient to the patient. The data is free. The math is known. The alpha is in the integration."

Built for Son of Anton.
