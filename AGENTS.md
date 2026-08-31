# Repository Working Rules

## Project

- This is a Python-based Toss Securities Open API quantitative trading and research project.
- The project is currently moving from an exploratory prototype toward a reliable research backtester.
- Paper trading and, eventually, live trading are long-term goals. Research and backtest reliability take priority now.
- The primary research objective is systematic discovery, falsification, and validation of quantitative alpha signals under the Alpha Lab protocol, not unconstrained Sharpe maximization.
- Publication research remains a secondary filter: repeated, economically interesting Alpha Lab findings may become Paper Observations and enter PQD, but an alpha result is not automatically a paper.
- Before evaluating a new alpha, assign an immutable ID and freeze an Alpha Card with its hypothesis, formula, information timing, data, metrics, costs, expected sign, and failure criteria.
- Preserve every tested hypothesis and failed result. Do not silently delete IDs, hide parameter variants, or relabel optimization output as discovery evidence.

## Safety — Critical

- Never execute a real order unless the user explicitly requests that exact action.
- Never call `buy_stock()`, `sell_stock()`, or a live order endpoint on your own.
- Live trading must be disabled by default and require an explicit, deliberate opt-in.
- Never read out, print, copy, or log the contents of `.env` or credentials.
- Never expose `CLIENT_ID`, `CLIENT_SECRET`, access tokens, account numbers, or equivalent sensitive values.
- Before changing order-related code, review every possible accidental-execution path, including import-time side effects and unsafe defaults.
- Keep backtest/paper execution and live broker execution clearly separated.

### Live Trading Confirmation

- A general development request such as "develop live trading" is not permission to execute a real order.
- Executing a live order requires a separate, explicit user confirmation for that specific order.
- Reviewing, refactoring, testing, or simulating order code does not constitute permission to execute a real order.

## API

- Design API calls with explicit timeouts, response validation, and exception handling.
- Do not assume that an API response matches the expected schema; validate status, content type, required fields, nulls, and value ranges.
- Handle the datatype and unit of prices, quantities, currencies, timestamps, and account identifiers explicitly.
- Do not run tests that call an external API without the user's permission.

## Backtest Principles

- Do not permit look-ahead bias.
- A signal produced from a closing price must not be filled at that same closing price.
- Keep the signal timestamp and execution timestamp explicit and distinct.
- Make transaction costs and slippage configurable parts of the execution model.
- Follow point-in-time data principles, especially for fundamentals and universe membership.
- State possible survivorship bias whenever the data cannot rule it out.
- Implement portfolio accounting from accurate cash, positions, cost basis, realized P&L, and unrealized P&L.
- Treat benchmarks and risk-adjusted metrics as standard evaluation outputs in future backtest work.
- Do not optimize a strategy solely from in-sample performance. Use out-of-sample or walk-forward validation where practical.

## Development

- Use Python for application and research code.
- Do not keep creating duplicated strategy version files.
- Prefer one engine with explicit configuration or parameters when practical.
- Prefer small functions and clear module responsibilities.
- Add tests for new core functionality and for fixes to portfolio accounting, timing, and order safety.
- When changing existing behavior, explain why it changed and what may be affected.
- Perform large refactors as small, independently verifiable steps.

## Testing

- Unit tests must not depend on the real broker API.
- Use mock or fake broker responses where practical.
- Keep integration tests that communicate with the real broker clearly separated from ordinary unit tests, and do not run them without explicit user permission.

## Alpha Research

- Separate signal discovery from signal combination and portfolio construction.
- Use cross-sectional IC, rank IC, coverage, quantile monotonicity, decay, turnover, concentration, and cost robustness as appropriate; portfolio CAGR alone is not alpha evidence.
- Record every tested hypothesis and variant in `research/alpha_lab/ALPHA_CATALOG.csv` with monotonic IDs and lineage.
- Treat parameter search as a separately approved optimization phase with a frozen search budget and multiple-testing controls.
- Label 2007–2022 as previously observed research history and keep Final OOS 2023–2025 sealed.
- Do not represent Yahoo/current-member histories as survivorship-free or point-in-time universes.

## Git

- Check `git status` before starting work.
- Preserve unrelated user changes and never revert them without explicit permission.
- Do not commit `.env`, `.env.*`, `.venv`, `__pycache__`, `*.pyc`, tokens, account data, or credentials.
- Do not create commits or push changes unless the user explicitly asks.
- Do not run destructive Git operations such as `git reset --hard`, force push, branch deletion, or history rewriting without explicit user permission.
- After work, report changed files and the important diff.
- When commits are requested, prefer one logical commit per work objective.

## Execution

- Read-only repository exploration commands may be used freely.
- Safe unit tests and static analysis may be run during development when they cannot call broker services or place orders.
- Treat any test that contacts the real broker API as an external integration test requiring explicit user permission.
- Never execute a command that could place a live order unless the user explicitly requested and confirmed it.

## Communication

After completing work, briefly report:

1. What changed
2. Why it changed
3. Which files changed
4. Which tests were run
5. Remaining risks or issues
6. Recommended next work
