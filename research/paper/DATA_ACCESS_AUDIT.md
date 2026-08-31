# Data Access Audit

| Source | Access | History/coverage | Contract/roll metadata | Reproducibility and restrictions | Verdict |
|---|---|---|---|---|---|
| Yahoo | Free | ETFs/indexes; history depends on listing | No futures roll/multiplier | Convenient but adjustment provenance/licensing weak | Pilot only |
| Stooq | Free | Long indexes and some futures proxies | Continuous methodology not always sufficient | Reproducible downloads; metadata audit needed | Pilot/control |
| FRED | Free | Macro, rates and selected financial series | No broad tradable futures panel | Stable series IDs and citations | State variables only |
| Kenneth French Library | Free | Equity factors from 1926 | Portfolio methodology documented | Strong citation/reproducibility | Controls only |
| Exchange public files | Mixed/free fragments | Exchange-specific | Often expiry/multiplier available | Historical depth and formats inconsistent | Verification source |
| CME DataMine | Paid | CME products; some history from 1972 | Official settlements and reference data; dataset-dependent | Licensed export; costs require quote/catalog | Strong but incomplete global breadth |
| Bloomberg | University candidate | Broad global futures/indexes | Continuous contracts and reference fields | Entitlement/export limits; query manifest essential | Strong if accessible |
| LSEG Workspace/Datastream | University candidate | Broad international futures and total-return indexes | Vendor continuous series and contract identifiers | Methodology/licensing must be archived | Strong if accessible |
| WRDS/CRSP | University candidate | Research-grade US securities | Excellent corporate-action/delisting treatment; not global futures | Institution-specific subscriptions | Equity controls |
| Commercial futures vendor | Paid | Broad contract-level history | Usually strong rolls/multipliers | Cost and publication license unknown | Best data; access unresolved |

No source was purchased, subscribed to or downloaded. University access is not assumed.

## Free-data Alternative

`NARROW ONLY`: a public ETF/index paper could study whether matched-volatility attribution is
sensitive to the choice of decomposition in listed multi-asset proxies. It could not claim to explain
global managed-futures trend decay or structural instability. A minimum Tier C version needs a
pre-defined ETF universe, total returns, public state variables, transparent costs and explicit
short-history/external-validity limitations.
