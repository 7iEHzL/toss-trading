# Q06 Factor-vintage Identification

## Two distinct treatments

- `MacroVintage`: which official macro history is used—real-time information or later revised history.
- `FactorVintage`: which downloaded/reconstructed factor history is used.

Akey, Robertson and Simutin show that changing only FactorVintage can materially change alphas,
loadings and model tests. This establishes a second measurement dimension; it does not make the two
dimensions equivalent.

## Claim audit

### Claim 1 — historical investability

“What information could a historical investor actually trade on?” requires contemporaneous macro and
factor construction, then-available security/accounting databases, methodology and release timing. A
modern FF reconstruction cannot establish this claim. Q06 must not make it.

### Claim 2 — modern researcher inference

“Holding one modern factor-return reconstruction fixed, how sensitive is historical conditional
inference to MacroVintage?” is coherent. The outcome is a fixed retrospective measurement and the
treatment is the researcher's macro information choice.

## Classification

**Factor-vintage interpretation: IDENTIFICATION ADVANTAGE, with a bounded limitation.**

Fixing FactorVintage is desirable for Claim 2 because it prevents a second changing input from
contaminating the MacroVintage contrast. The limitation is external: the result may differ under another
factor vintage, and it cannot be interpreted as the historical investor's tradeable factor experience.

## Conceptual 2×2

| | Macro real-time | Macro revised |
|---|---|---|
| Fixed modern FactorVintage | Core Q06 contrast | Core Q06 contrast |
| Alternative FactorVintage | Conceptual sensitivity only | Conceptual sensitivity only |

The lower row is useful for explaining two-dimensional measurement risk but is not necessary to identify
the fixed-vintage estimand. Expanding into a full 2×2 project would enlarge scope and could become a
specification search. It is not authorized by this audit.

## Required boundary if ever designed

Any later paper would have to record the factor download/reconstruction vintage, state that only
MacroVintage varies in the primary contrast, and characterize Akey-style FactorVintage instability as a
scope limitation. That preserves Claim 2 without pretending to answer Claim 1.
