"""Validation and deterministic selection for the pre-registered R4-000 audit."""

import math

import pandas as pd


AUDIT_START = pd.Timestamp("2013-01-01")
FREEZE_END_EXCLUSIVE = pd.Timestamp("2014-07-01")
FINAL_OOS_START = pd.Timestamp("2023-01-01")
INCEPTION_CUTOFF = pd.Timestamp("2010-01-01")
MIN_MEDIAN_DOLLAR_VOLUME = 5_000_000.0
MIN_CALENDAR_COVERAGE = 0.95


def validate_r4_price_frame(frame, ticker="unknown"):
    required = {"date", "open", "high", "low", "close", "raw_close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{ticker} missing columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError(f"{ticker} has no observations")
    dates = pd.to_datetime(frame["date"], errors="coerce")
    if dates.isna().any() or dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError(f"{ticker} dates must be valid, unique, and sorted")
    if dates.min() < AUDIT_START or dates.max() >= FREEZE_END_EXCLUSIVE:
        raise ValueError(f"{ticker} contains data outside the R4-000 audit interval")
    if (dates >= FINAL_OOS_START).any():
        raise ValueError(f"{ticker} contains Final OOS data")

    numeric = frame[["open", "high", "low", "close", "raw_close"]].apply(
        pd.to_numeric, errors="coerce"
    )
    if numeric.isna().any().any():
        raise ValueError(f"{ticker} prices must be numeric")
    if not numeric.map(math.isfinite).all().all() or (numeric <= 0).any().any():
        raise ValueError(f"{ticker} prices must be finite and positive")
    volume = pd.to_numeric(frame["volume"], errors="coerce")
    if volume.isna().any() or not volume.map(math.isfinite).all() or (volume < 0).any():
        raise ValueError(f"{ticker} volume must be finite and non-negative")
    tolerance = 1e-10
    if (numeric["high"] + tolerance < numeric[["open", "low", "close"]].max(axis=1)).any():
        raise ValueError(f"{ticker} high is inconsistent")
    if (numeric["low"] - tolerance > numeric[["open", "high", "close"]].min(axis=1)).any():
        raise ValueError(f"{ticker} low is inconsistent")


def audit_candidate(candidate, frame, reference_dates):
    ticker = candidate["ticker"]
    validate_r4_price_frame(frame, ticker)
    inception = pd.Timestamp(candidate["inception_date"])
    dates = pd.DatetimeIndex(pd.to_datetime(frame["date"]))
    reference_dates = pd.DatetimeIndex(reference_dates)
    periods = {
        "coverage_2013": ("2013-01-01", "2014-01-01"),
        "coverage_2014_h1": ("2014-01-01", "2014-07-01"),
    }
    coverage = {}
    for name, (start, end) in periods.items():
        expected = reference_dates[(reference_dates >= start) & (reference_dates < end)]
        observed = dates[(dates >= start) & (dates < end)]
        coverage[name] = len(observed.intersection(expected)) / len(expected) if len(expected) else 0.0
    in_2013 = frame[(dates >= pd.Timestamp("2013-01-01")) &
                    (dates < pd.Timestamp("2014-01-01"))]
    median_dollar_volume = float((in_2013["raw_close"] * in_2013["volume"]).median())
    passes = (
        inception < INCEPTION_CUTOFF
        and median_dollar_volume >= MIN_MEDIAN_DOLLAR_VOLUME
        and all(value >= MIN_CALENDAR_COVERAGE for value in coverage.values())
    )
    return {
        **candidate,
        "rows": int(len(frame)),
        "first_date": dates.min().strftime("%Y-%m-%d"),
        "last_date": dates.max().strftime("%Y-%m-%d"),
        "median_dollar_volume_2013": median_dollar_volume,
        **coverage,
        "eligible": bool(passes),
    }


def select_representatives(audit_frame):
    selected = []
    categories = sorted(audit_frame["category"].unique())
    for category in categories:
        eligible = audit_frame[(audit_frame["category"] == category) & audit_frame["eligible"]].copy()
        if eligible.empty:
            raise ValueError(f"no eligible R4 candidate for category: {category}")
        eligible["inception_date"] = pd.to_datetime(eligible["inception_date"])
        eligible = eligible.sort_values(
            ["median_dollar_volume_2013", "inception_date", "ticker"],
            ascending=[False, True, True], kind="mergesort",
        )
        selected.append(eligible.iloc[0])
    return pd.DataFrame(selected).sort_values("category").reset_index(drop=True)
