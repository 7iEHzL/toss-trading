# Alpha Lab v1 Research Protocol

## Objective

Alpha Lab systematically discovers, falsifies and validates cross-sectional alpha signals. It is a
discovery engine, not a Sharpe-maximization loop. Repeated, economically structured findings may be
forwarded to the publication-question-discovery (PQD) process; an alpha result is not automatically a
paper.

R1–R5, R3/R4 data audits, PQD and the Q06 `RED — KILL` verdict are immutable legacy evidence.

## Research cycle

`Hypothesis → Alpha Card → data gate → signal/forward-return construction → cross-sectional test →
robustness/falsification → decision → immutable catalog entry`

No performance may be viewed before an Alpha Card has an unused ID, fixed hypothesis, formula,
information timing, universe, horizon, costs, metrics and failure criteria.

## Discovery versus optimization

- **Discovery** asks whether one economically motivated signal contains expected-sign information under
  a single preregistered specification. Neighboring parameters are not searched.
- **Optimization** compares explicitly registered variants or combinations after a signal survives
  discovery. It requires separate approval, a frozen search budget and validation protocol.

Optimization results may not be relabeled as discovery evidence.

## Unit of research

The unit is `Axxx`, allocated monotonically. Variants use `Axxx-v01`, `Axxx-v02`, not new unrelated IDs.
Every ID remains in `ALPHA_CATALOG.csv`; failed or invalid experiments are never deleted.

Statuses:

- `PROPOSED`: concept only; no performance authorized.
- `PREREGISTERED`: card frozen; data gate may begin.
- `DATA_BLOCKED`: required information cannot pass its gate.
- `TESTED`: results recorded, decision pending.
- `REJECT`: falsified or practically unusable under frozen criteria.
- `HOLD`: informative but insufficient evidence.
- `CANDIDATE`: passes discovery and validation gates; not deployment approval.
- `INVALIDATED`: leakage, data or implementation defect makes the test unusable.

## Stage separation

1. Signal discovery: evaluate `S(i,t)` against `R(i,t+h)`.
2. Signal combination: only separately approved nonredundant candidates.
3. Portfolio construction: test implementability after costs.

A portfolio CAGR cannot establish alpha, and one arbitrary portfolio cannot by itself falsify a
predictive signal.

## Decision classes

- `REJECT`: wrong-sign primary evidence, structurally poor coverage, non-monotone/noisy spread with no
  corroboration, or instability/dependence that defeats the hypothesis.
- `WEAK`: expected sign appears but is economically/statistically fragile or highly dependent.
- `INTERESTING`: expected-sign IC plus corroborating monotonicity/stability/coverage evidence; independent
  validation still absent.
- `CANDIDATE`: preregistered validation, costs, time/universe robustness and concentration diagnostics all
  support the signal.

Numeric gates must be frozen after the universe/data audit and before A001 is tested. They must not be
chosen from prior Alpha Lab outcomes.

## Safety and stop rules

- Final OOS 2023–2025 remains sealed and outside Alpha Lab.
- Broker endpoints, live orders and credentials are never part of research execution.
- No silent ticker removal, imputation, winsorization or universe change.
- Any leakage, timestamp failure or snapshot mismatch invalidates the affected run.
- Alpha Lab v1 is design-only: A001–A010 performance is not authorized.

## Planned directory structure

```text
research/alpha_lab/
├── ALPHA_RESEARCH_PROTOCOL.md
├── ALPHA_CATALOG.csv
├── ALPHA_FAMILIES.md
├── WORLDQUANT_RESEARCH_MODEL.md
├── DATA_FEASIBILITY.md
├── UNIVERSE_OPTIONS.md
├── TEMPORAL_PROTOCOL.md
├── METRICS_AND_INFERENCE.md
├── MULTIPLE_TESTING_POLICY.md
├── PAPER_DISCOVERY_BRIDGE.md
├── INITIAL_ALPHA_BATCH.md
├── cards/                 # frozen cards and template
├── experiments/           # future immutable run metadata/results
├── diagnostics/           # common data/signal diagnostics
├── candidates/            # references, never the only copy of results
├── rejected/              # references preserving failed evidence
└── paper_observations/    # observations awaiting PQD
```

Only the protocol, catalog and templates are created in v1. Empty operational directories wait for the
minimum engine so that unused scaffolding does not imply implemented capability.
