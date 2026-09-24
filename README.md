# BoxOffice

**An AI-native marketplace finance, trust & operations platform + evaluation layer — built for SeatGeek.**

BoxOffice is a backend that does the AI-money-and-trust work a live-event ticketing
marketplace has to get right, and adds the one thing that makes shipping it safe: a way
to **measure** whether the AI is correct. It spans payment fraud, bot/scalper collusion
rings, chargebacks, marketplace spend, settlement-float treasury, vendor/partner
payouts, and partner credit — each backed by a real ML model — and grades every agent
decision against ground truth on a **multi-model leaderboard**.

It runs **fully offline** on deterministic ML; set `ANTHROPIC_API_KEY` and the eval
leaderboard lights up with live **Claude Opus 4.8 / Sonnet 4.6 / Haiku 4.5**.

```bash
python -m venv .venv && .venv/Scripts/pip install -e .   # (Linux/Mac: .venv/bin/pip)
boxoffice serve          # → http://127.0.0.1:8000/dashboard
boxoffice demo           # or: full narrated CLI showcase
```

---

## Why it's built for SeatGeek

SeatGeek is a two-sided live-event marketplace: millions of fans buying tickets on
cards, thousands of sellers and venue partners getting paid out, and hot on-sales that
draw exactly the abuse a marketplace fears — **card fraud, account takeover, and
bot/scalper rings** that share devices and IPs to sweep inventory. The money that flows
through it is real and time-critical: buyer funds settle, the float is held until the
event, and sellers are paid out after. Getting fraud, chargebacks, payouts, and cash
forecasting right — at on-sale speed — is the core operational problem.

Every one of those surfaces is now an AI surface, which raises the question SeatGeek's
Trust & Safety and Finance teams actually have to answer before shipping: *is the model
right?* BoxOffice builds the surfaces **and** ties them together with the correctness
layer:

> **It grades every agent decision against held-out ground truth before it goes
> live — a promotion gate, not a vibe check.**

---

## The platform — 9 surfaces

| Tab | What it does | ML / method |
|---|---|---|
| **Overview** | Exec roll-up + a single "value identified" tally | aggregates everything |
| **Fraud & Risk** | Alerts, bot/scalper collusion rings, causal explanations | Isolation Forest + GBM + graph |
| **Spend & Expense** | Categories, vendor subscriptions, duplicates, policy compliance, anomalies | cadence detection + rules |
| **Treasury · Cash** | Settlement-float + operating-cash forecast, runway, idle-cash yield sweep | Ridge forecaster (backtested) |
| **Bill Pay · AP** | Duplicate vendor invoices, partner concentration, payout timing | dedup + HHI + float math |
| **Credit** | Dynamic partner/seller trust limit + probability-of-loss | Gradient-boosted PD model |
| **Agents** | Orchestrator + autonomous fraud investigation | agent mesh + tools |
| **Benchmark** | Financial-correctness leaderboard (the promotion gate) | eval harness + bootstrap CI |
| **Models** | A card per model with its live metric | the architecture story |

---

## The ML portfolio (live, honest metrics)

| Model | Type | Task | Metric |
|---|---|---|---|
| Fraud Ensemble | Isolation Forest + Gradient Boosting | payment fraud | **ROC-AUC ≈ 0.95** (0.89 ± 0.08 5-fold CV) |
| Partner-Risk PD | Gradient Boosting | payout/chargeback loss | **ROC-AUC ≈ 0.94** |
| Treasury Forecaster | Ridge (calendar + lag) | cash-flow / runway | **backtest MAPE ≈ 10%** |
| Collusion-Ring Graph | networkx components | bot/scalper rings | shared-device clusters |
| Causal Explainer | counterfactual do-operator | fraud explanation | per-alert drivers |
| Recurring detector | inter-arrival cadence | vendor subscriptions | redundant-license savings |

The data is engineered to be *hard* — legit partner travel on trusted devices, shared
office IPs, account-takeover fraud that rides the buyer's own device, merchant-risk
overlap — so nothing is a trivial oracle and the models have to learn interactions.
Metrics are credible, not synthetic-perfect.

---

## Headline capabilities

**Fraud & graph intelligence** — a blended anomaly + supervised ensemble over
behavioral-biometric, velocity and **graph** features. Links cards by shared devices and
cross-metro IPs to surface **bot/scalper collusion rings** — the multi-account,
shared-infrastructure abuse that sweeps a hot on-sale (office VPNs excluded so shared
infra isn't mistaken for a ring). Every alert gets **counterfactual causal drivers** ("if
geo-velocity were normal, risk drops 0.42") and an action: freeze the card, open a
chargeback dispute, monitor, clear.

**Treasury & cash-flow forecasting** — reconstructs the daily balance across operating
cash and the marketplace settlement float, and forecasts it forward with a backtested
confidence band; computes runway, a liquidity-shortfall date, and an **idle-cash yield
sweep** into an overnight money-market fund (~4% APY).

**Dynamic partner/seller-trust underwriting** — a gradient-boosted probability-of-loss
model (AUC ≈ 0.94) on a synthetic partner portfolio: how likely a counterparty is to
generate a payout or chargeback loss, a cash-coverage limit recommendation, and a dynamic
action (raise / hold / reduce-within-24h) — trust limits scale up as history builds and
can be cut fast for at-risk accounts.

**Spend & AP intelligence** — recurring-subscription detection with redundant-license
consolidation savings, duplicate-charge recovery, policy-compliance scoring, plus AP
duplicate-invoice detection, vendor/partner-concentration (HHI) risk, and payout timing
that holds cash in the MMF until due while capturing 2/10-net-30 discounts.

**Agentic workflows** — narrow single-task agents (categorize, audit policy, triage
fraud, adjudicate chargebacks, reconcile expense reports) plus a **BoxOfficeOrchestrator**
that sequences them and escalates to a full **FraudInvestigator** workflow, all running
on any backend (deterministic, simulated, or live Claude).

**Financial-correctness benchmark** — the promotion gate. Five tasks (GL coding, policy
set-F1, chargeback adjudication, fraud triage, tieout-to-the-cent) graded against held-out
ground truth with bootstrap confidence intervals, cost and latency. The deterministic
engine is the reference; models are ranked on how faithfully they reproduce a
controller's judgment.

```
Financial-correctness leaderboard (offline run)
 backend                 kind          overall   cost     ms
 offline-heuristic       deterministic   1.000   $0.000     0   ← reference
 claude-opus-4-8 (sim)   simulated       0.974   ...
 claude-sonnet-4-6 (sim) simulated       0.928   ...
 claude-haiku-4-5 (sim)  simulated       0.862   ...
```

---

## Run it

```bash
boxoffice serve                 # multi-tab dashboard + API (http://127.0.0.1:8000)
boxoffice demo                  # narrated end-to-end CLI showcase
boxoffice fraud                 # fraud metrics, alerts, rings
boxoffice orchestrate --top     # full agent decision on the top alert
boxoffice eval --task-detail    # the benchmark leaderboard
```

API (all surfaces are one call away):

```
GET  /overview                    # exec roll-up + value identified
GET  /fraud/alerts  /fraud/rings  /fraud/assess/{txn}
GET  /treasury/forecast  /credit/underwrite
GET  /spend/intelligence  /ap/intelligence  /models
POST /agent/orchestrate  /eval/run
GET  /agent/investigate/{txn}     ·   docs at /docs
```

---

## Going live with Claude

Set `ANTHROPIC_API_KEY` and the simulated leaderboard rows become real graded models —
called through the Anthropic SDK with **structured outputs**, **adaptive thinking**, and
**effort** (Opus 4.8 / Sonnet 4.6 think adaptively; Haiku 4.5 runs lean). Cost and
latency are tracked per call, so the board answers *which model is most correct, at what
price* — the data you need to route traffic on a production LLM gateway.

---

## Repo layout

```
boxoffice/
  domain/      marketplace primitives (Card, Cash, chargebacks, policy) + the rule engine
  data/        deterministic synthetic-tenant generator (fraud, subscriptions, GT)
  fraud/       entity graph · features · ML ensemble · causal explainer · pipeline
  analytics/   forecasting · underwriting · spend · ap · model registry
  agents/      5 evaluable agents + orchestrator + investigator + tools
  llm/         backend abstraction: analytical · simulated · live Claude
  eval/        scorers · tasks · harness · leaderboard
  api/         FastAPI service + the multi-tab dashboard
  reporting.py · cli.py
scripts/       demo · train_fraud (CV) · run_eval
tests/         offline test suite
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the design deep-dive. Everything is
deterministic and reproducible from a seed; the ML trains, the agents run, the eval
grades — nothing here is a mock.

Built by Harsh Vardhan as a SeatGeek-specific demonstration of production-quality
AI marketplace-trust + evaluation engineering.
