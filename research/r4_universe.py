"""Build the R4-000 eligibility snapshot. This module never runs strategy performance."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from data.r4_validator import audit_candidate, select_representatives
from data.sources.r4_yahoo_price_source import R4YahooPriceSource


CANDIDATE_PATH = Path("research/R4_CANDIDATES.csv")
DEFAULT_OUTPUT = Path("data/snapshots/r4/r4_000_fixed_etf_audit_v1")


def build_r4_000_snapshot(output_dir=DEFAULT_OUTPUT, source=None):
    source = source or R4YahooPriceSource()
    candidates = pd.read_csv(CANDIDATE_PATH, dtype=str)
    _validate_candidates(candidates)
    output_dir = Path(output_dir)
    prices_dir = output_dir / "prices"
    prices_dir.mkdir(parents=True, exist_ok=True)

    prices = {}
    failures = {}
    for ticker in candidates["ticker"]:
        try:
            prices[ticker] = source.download(ticker)
        except (KeyError, ValueError, RuntimeError) as exc:
            failures[ticker] = str(exc)
    if "SPY" not in prices:
        raise ValueError("SPY reference calendar is unavailable")
    reference_dates = pd.DatetimeIndex(prices["SPY"]["date"])
    audits = []
    for _, row in candidates.iterrows():
        candidate = row.to_dict()
        ticker = candidate["ticker"]
        if ticker in prices:
            result = audit_candidate(candidate, prices[ticker], reference_dates)
            result["download_error"] = ""
        else:
            result = {**candidate, "rows": 0, "first_date": "", "last_date": "",
                      "median_dollar_volume_2013": float("nan"),
                      "coverage_2013": 0.0, "coverage_2014_h1": 0.0,
                      "eligible": False, "download_error": failures[ticker]}
        audits.append(result)
    audit = pd.DataFrame(audits)
    universe = select_representatives(audit)

    for ticker, frame in prices.items():
        frame.to_csv(prices_dir / f"{ticker}.csv", index=False, date_format="%Y-%m-%d")
    audit.to_csv(output_dir / "candidate_audit.csv", index=False)
    universe.to_csv(output_dir / "selected_universe.csv", index=False)
    metadata = {
        "snapshot_id": "r4_000_fixed_etf_audit_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "Yahoo Finance via yfinance",
        "source_version": source.version,
        "requested_start": "2013-01-01",
        "requested_end_exclusive": "2014-07-01",
        "liquidity_definition": "median(raw close * volume) on 2013 observations",
        "performance_run": False,
        "final_oos_downloaded": False,
        "selected_tickers": universe["ticker"].tolist(),
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    files = sorted(path for path in output_dir.rglob("*") if path.is_file()
                   and path.name != "manifest.sha256")
    manifest = "\n".join(f"{_sha256(path)}  {path.relative_to(output_dir).as_posix()}"
                         for path in files) + "\n"
    (output_dir / "manifest.sha256").write_text(manifest, encoding="utf-8")
    return audit, universe, metadata


def _validate_candidates(frame):
    required = {"category", "ticker", "inception_date", "exposure", "issuer_source"}
    if required.difference(frame.columns) or frame.empty:
        raise ValueError("invalid R4 candidate roster")
    if frame["ticker"].duplicated().any():
        raise ValueError("R4 candidate tickers must be unique")
    if (pd.to_datetime(frame["inception_date"]) >= pd.Timestamp("2010-01-01")).any():
        raise ValueError("candidate roster violates inception cutoff")
    if frame["category"].nunique() != 9:
        raise ValueError("R4 candidate roster must contain exactly nine categories")


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    _, universe, metadata = build_r4_000_snapshot()
    print(json.dumps({"selected_tickers": universe["ticker"].tolist(), **metadata}, indent=2))


if __name__ == "__main__":
    main()
