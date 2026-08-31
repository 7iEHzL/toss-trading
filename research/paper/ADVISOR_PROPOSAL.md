# Advisor-ready Proposal

## Working Title

When Trend Components Break: Directional Predictability, Dynamic Risk Allocation, and Their Interaction

## Question and Motivation

When trend-following performance changes, is the variation associated with directional return
predictability, dynamic risk allocation, or their interaction after assets, exposure, risk and costs
are matched? Finance researchers care because these channels imply different explanations for
momentum and different expectations about robustness.

## Literature and Potential Gap

Existing research separately questions directional TSMOM predictability, shows that volatility
scaling drives reported performance, and documents instability in volatility-managed portfolios.
Recent working papers also provide exact trend P&L decompositions and explain post-2009 decay.
Therefore a generic decomposition or decay result is not novel. The only possible gap is a formal,
matched joint-stability test with a separately identified interaction and an independently motivated
state variable.

## Proposed Design

Define four ex-ante portfolios crossing dynamic/fixed signal exposure with dynamic/fixed allocation,
matched on leverage and risk. Estimate signal, allocation and difference-in-differences interaction
contrasts in a broad futures panel. Use continuous state interactions as the primary stability design,
HAC/two-way clustered inference, block bootstrap and multiplicity control. Unknown-break results
would be diagnostic only.

## Data

The preferred dataset contains 40+ years and 50–100 global futures contracts with raw settlement,
expiry, multiplier, currency, rolls, financing and cost proxies. Bloomberg, LSEG/Datastream or a
commercial futures source may work if university access and reproducibility rights exist. Free ETF
data support only a narrower student paper.

## Biggest Concern

The economic mechanism is unresolved, and 2026 working papers create a high novelty threat. Joint
estimation is insufficient unless it tests a new restriction or mechanism. R5 provides only one
contaminated pilot motivation and is not publication evidence.

## Questions for Advisor

1. Is the matched factorial interaction an economic contribution or only measurement hygiene?
2. Which single mechanism/state variable has a defensible theoretical prior?
3. Does the university provide reproducible global futures data and permit research exports?
