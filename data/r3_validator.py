"""Pre-registered quality checks for the free-data R3 snapshot."""

import pandas as pd


FINAL_OOS_START = pd.Timestamp("2023-01-01")
MIN_MEMBERS = 480
MAX_MEMBERS = 520
MIN_PRICE_COVERAGE = 0.98
MIN_MAPPING_COVERAGE = 0.99
MAX_SECONDARY_MISMATCH = 0.02


def validate_membership(frame):
    required = {"as_of", "ticker", "membership_status", "membership_source"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"membership missing columns: {', '.join(sorted(missing))}")
    dates = pd.to_datetime(frame["as_of"], errors="coerce")
    if dates.isna().any() or (dates >= FINAL_OOS_START).any():
        raise ValueError("membership contains invalid or Final OOS dates")
    if frame.duplicated(["as_of", "ticker"]).any():
        raise ValueError("membership contains duplicate date/ticker rows")
    counts = frame.groupby(dates)["ticker"].nunique()
    if (counts < MIN_MEMBERS).any() or (counts > MAX_MEMBERS).any():
        raise ValueError("membership constituent count is outside 480-520")
    return {"snapshot_count": int(len(counts)), "min_count": int(counts.min()),
            "max_count": int(counts.max())}


def validate_price_frame_r3(frame, ticker):
    required = {"date", "open", "high", "low", "close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{ticker} missing columns: {', '.join(sorted(missing))}")
    dates = pd.to_datetime(frame["date"], errors="coerce")
    if dates.isna().any() or dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError(f"{ticker} dates must be valid, unique, and sorted")
    if (dates >= FINAL_OOS_START).any():
        raise ValueError(f"{ticker} contains Final OOS data")
    numeric = frame[["open", "high", "low", "close"]].apply(pd.to_numeric, errors="coerce")
    finite = numeric.map(lambda value: pd.notna(value) and abs(value) != float("inf"))
    if numeric.isna().any().any() or not finite.all().all():
        raise ValueError(f"{ticker} OHLC must be finite")
    if (numeric <= 0).any().any():
        raise ValueError(f"{ticker} OHLC must be positive")
    if (numeric["high"] < numeric[["open", "low", "close"]].max(axis=1)).any():
        raise ValueError(f"{ticker} high is inconsistent")
    if (numeric["low"] > numeric[["open", "high", "close"]].min(axis=1)).any():
        raise ValueError(f"{ticker} low is inconsistent")


def coverage_report(membership, prices, mapping_status):
    requested = sorted(set(membership["ticker"]))
    available = sorted(t for t in requested if t in prices and not prices[t].empty)
    missing = sorted(set(requested).difference(available))
    exact_or_mapped = sum(mapping_status.get(t) in {"exact", "mapped"} for t in requested)
    requested_count = len(requested)
    price_ratio = len(available) / requested_count if requested_count else 0.0
    mapping_ratio = exact_or_mapped / requested_count if requested_count else 0.0
    constituent_dates = constituent_date_coverage(membership, prices)
    return {
        "requested_constituent_count": requested_count,
        "price_available_count": len(available), "missing_count": len(missing),
        "price_coverage_ratio": price_ratio, "membership_coverage_ratio": 1.0,
        "mapping_coverage_ratio": mapping_ratio,
        "constituent_date_coverage_ratio": constituent_dates["coverage_ratio"],
        "requested_constituent_dates": constituent_dates["requested"],
        "available_constituent_dates": constituent_dates["available"],
        "unresolved_ticker_count": requested_count - exact_or_mapped,
        "missing_tickers": missing,
        "price_gate_passed": price_ratio >= MIN_PRICE_COVERAGE,
        "mapping_gate_passed": mapping_ratio >= MIN_MAPPING_COVERAGE,
    }


def constituent_date_coverage(membership, prices):
    """Measure usable price rows over PIT membership states.

    The trading calendar is the union of all available price dates. Sparse
    membership snapshots are carried forward only until the next change date.
    """
    if membership.empty or not prices:
        return {"requested": 0, "available": 0, "coverage_ratio": 0.0}
    calendar = pd.DatetimeIndex(sorted(set().union(*(
        set(pd.to_datetime(frame["date"])) for frame in prices.values()
    ))))
    states = [(pd.Timestamp(date), set(group["ticker"]))
              for date, group in membership.groupby("as_of", sort=True)]
    price_dates = {ticker: set(pd.to_datetime(frame["date"]))
                   for ticker, frame in prices.items()}
    requested = available = 0
    for index, (start, members) in enumerate(states):
        end = states[index + 1][0] if index + 1 < len(states) else FINAL_OOS_START
        active_dates = calendar[(calendar >= start) & (calendar < end)]
        requested += len(active_dates) * len(members)
        for ticker in members:
            dates = price_dates.get(ticker, set())
            available += sum(date in dates for date in active_dates)
    ratio = available / requested if requested else 0.0
    return {"requested": requested, "available": available,
            "coverage_ratio": ratio}


def classify_audit(coverage, hashes_valid, secondary_verified=False,
                   secondary_mismatch_ratio=None):
    if (not hashes_valid or not coverage["price_gate_passed"]
            or not coverage["mapping_gate_passed"]):
        return "BLOCKED — DATA QUALITY INSUFFICIENT"
    if (not secondary_verified or secondary_mismatch_ratio is None
            or secondary_mismatch_ratio > MAX_SECONDARY_MISMATCH):
        return "CONDITIONAL — LIMITED REPLICATION ONLY"
    return "PASS — FREE-DATA REPLICATION AUTHORIZED"
