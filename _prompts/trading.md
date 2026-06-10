---
category: trading
tags: [prompts, trading, prop-firm, prediction-markets, strategy, risk]
ai-first: true
---

## For future Claude
Prompts for trading strategy design, risk management, and bot architecture.

---

## prompt: Trading Strategy Auditor
**use-when**: strategy is losing money, prop firm account blown, need to diagnose why
**template**:
Audit this trading strategy: [STRATEGY_DESCRIPTION]. I'm trading [INSTRUMENT] on [TIMEFRAME]. Recent results: [RECENT_RESULTS]. Diagnose: is this a risk management failure, entry timing failure, or strategy edge failure? Give me a 3-point fix with specific rule changes.

**variables**:
- STRATEGY_DESCRIPTION: describe your entry/exit rules
- INSTRUMENT: what you're trading (NQ futures, BTC prediction markets, crypto, stocks)
- TIMEFRAME: 5min, 15min, daily, etc.
- RECENT_RESULTS: recent P&L or what happened

---

## prompt: Prop Firm Rule Checker
**use-when**: before placing a trade on a funded account, or before buying a new evaluation
**template**:
I have a [FIRM_NAME] [ACCOUNT_TYPE] funded account. Rules: daily max loss [DAILY_LIMIT], total drawdown [TOTAL_LIMIT], [OTHER_RULES]. My planned trade is [TRADE_DESCRIPTION]. Does this trade risk violating any rules? What's the maximum safe position size?

**variables**:
- FIRM_NAME: e.g. TopStep, Apex, FTMO, MyFundedFutures
- ACCOUNT_TYPE: e.g. Pro 50K, Challenge 100K
- DAILY_LIMIT: e.g. $2,500
- TOTAL_LIMIT: e.g. $5,000
- OTHER_RULES: any additional rules (no news trading, minimum hold time, etc.)
- TRADE_DESCRIPTION: instrument, direction, size you're considering

---

## prompt: Prediction Market Strategy Designer
**use-when**: designing a new prediction market trading strategy, backtesting approach
**template**:
Design a prediction market strategy for [MARKET_TYPE] markets on [PLATFORM]. I want to exploit: [EDGE_HYPOTHESIS]. Available data: [DATA_SOURCES]. Risk constraints: max [MAX_POSITION]% of bankroll per trade, max [MAX_DRAWDOWN]% daily drawdown. Give me entry rules, exit rules, and a backtest framework.

**variables**:
- MARKET_TYPE: e.g. BTC price markets, election markets, sports, economic indicator markets
- PLATFORM: Kalshi, Polymarket, or both
- EDGE_HYPOTHESIS: what edge you think exists
- DATA_SOURCES: what data you have access to
- MAX_POSITION: e.g. 5
- MAX_DRAWDOWN: e.g. 10

---

## prompt: Deep Research Dive
**use-when**: going deeper on a specific trader, strategy, platform, or tool after an initial overview
**template**:
Research [SUBJECT] in depth. I already know: [WHAT_I_KNOW]. I want to understand: [SPECIFIC_QUESTIONS]. Focus on: practical mechanics, real numbers, verified claims vs. marketing copy. Separate confirmed facts from speculation. Give me a verdict at the end: is [SUBJECT] worth my time/money given my context: [MY_CONTEXT].

**variables**:
- SUBJECT: the trader, strategy, tool, or platform to research
- WHAT_I_KNOW: brief summary of what's already in context
- SPECIFIC_QUESTIONS: the exact gaps to fill
- MY_CONTEXT: your situation (budget, goals, risk tolerance)

---

## prompt: Risk Management Framework
**use-when**: sizing positions, setting stop losses, building a mechanical kill switch
**template**:
Build a risk management framework for [TRADING_SETUP]. Account size: [ACCOUNT_SIZE]. My biggest weakness: [WEAKNESS]. I need: hard daily stop loss rule, position sizing formula, and a kill switch condition. Make it entirely mechanical — no discretion required at execution time.

**variables**:
- TRADING_SETUP: describe your setup (prop firm, personal capital, algo vs manual, platform)
- ACCOUNT_SIZE: funded account or personal capital size
- WEAKNESS: e.g. "I overtrade after losses", "I hold losers too long", "I revenge trade"
