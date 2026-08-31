# Q06 Information-set Feasibility

## Verdict

**CONDITIONAL.** Public infrastructure can reconstruct many vintage values, but a vintage value alone
does not prove its exact availability at a decision timestamp.

ALFRED exposes observations by real-time period/vintage date. The Philadelphia Fed RTDSM exposes full
historical vintages and, for selected series, documented first-, second- and third-release values. FRED's
own API warns that source release dates do not necessarily equal availability dates on FRED/ALFRED.

## Required fields

Every observation would need:

- reference period;
- statistical release and actual release date;
- archive vintage date and value available at the decision date;
- first, subsequent, seasonal and benchmark revisions;
- documented definition/base/classification changes;
- transformation performed only from values available in that vintage.

“Lag by one month” is not a valid substitute for this mapping.

## Data-quality ranking only

No variable is selected here. Ranking reflects archive and timing transparency, not expected asset-
pricing significance.

| Rank band | Candidate series | Data/identification assessment |
|---|---|---|
| 1 | Payroll employment / employment releases | Strong RTDSM release/revision documentation and meaningful revisions; annual benchmark revisions require explicit treatment |
| 1 | Industrial production | Long monthly vintage tradition and revisions; definition/benchmark changes require metadata checks |
| 2 | Real GDP/GNP | Rich quarterly vintage history and first/second/third releases; low frequency, benchmark revisions and historical GNP/GDP definition changes complicate a small project |
| 2 | Unemployment rate | Clear monthly release calendar; seasonal adjustment and underlying household-survey revisions must be distinguished |
| 3 | CPI | Clear release calendar, but revision behavior differs sharply between seasonally adjusted and unadjusted series; treatment strength must not drive selection |
| Avoid as primary without special audit | Derived output gaps, CFNAI before its real-time inception, composite PCs | Vintage of inputs, changing filters/weights and pseudo-history add researcher reconstruction choices |

## Reproducibility gate

Feasibility passes only if a candidate series can be reconstructed using documented vintages and a
conservative decision-time rule without hand-coded exceptions chosen after factor results. Definition
changes must be versioned, and transformed growth/state variables must be recomputed inside each
vintage. Otherwise K5 applies.

This audit does not select a series, date, regime or transformation and does not authorize downloads.
