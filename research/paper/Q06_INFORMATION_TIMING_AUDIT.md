# Q06 Information-timing Audit

## Macro Side

`InformationSet(t)` must use observations with release timestamp `<= t`, selecting the latest vintage
available then. Reference period, observation date, release date, vintage date and revision date are
distinct fields. Monthly lagging is not sufficient when releases occur mid-month or are revised before
decision dates. Seasonal and benchmark revisions must remain excluded from the real-time branch.

Feasibility: `CONDITIONAL`. ALFRED/Philadelphia Fed archives can support many series, but early
vintages, exact release calendars and series-definition changes need a data-only audit.

## Factor Side

Today's French factor history can defensibly be treated as a reconstructed realized-return outcome
conditional on investors' historical macro information. It cannot be described as the factor portfolio
an investor observed exactly in today's reconstructed form.

Risks include constituent/accounting timing, delistings, CRSP corrections, linking-table changes and
retroactive factor-method changes. Akey, Robertson & Simutin (2026) show economically material
factor-vintage changes. Therefore “change ONLY macro vintage” is conditional on explicitly fixing one
outcome vintage and narrowing the claim to researcher inference, not contemporaneous tradability.

Overall information-set feasibility: `CONDITIONAL`, not PASS.
