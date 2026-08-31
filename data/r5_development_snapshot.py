"""Build and validate the sealed pre-2015 R5 development snapshot."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from data.r3_validator import validate_price_frame_r3
from data.snapshot import DataSnapshot
from data.yfinance_source import _normalize_download


R5_UNIVERSE = ("SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "IYR", "GLD", "DBC")
START = "2006-02-03"
END_EXCLUSIVE = "2015-01-01"
EVALUATION_START = "2007-03-01"
LATEST_ACCEPTABLE_FIRST_DATE = "2006-03-01"
MIN_COMMON_CALENDAR_COVERAGE = 0.95
DEFAULT_OUTPUT = Path("data/snapshots/r5/r5_000_2006_2014_data_gate_v1")


class R5YahooPriceSource:
    name = "Yahoo Finance via yfinance"

    def __init__(self, module=None):
        if module is None:
            import yfinance as module
        self._module = module

    @property
    def version(self):
        return getattr(self._module, "__version__", "unknown")

    def download(self, ticker, start=START, end_exclusive=END_EXCLUSIVE):
        if pd.Timestamp(start) < pd.Timestamp(START):
            raise ValueError("R5 request precedes the pre-registered boundary")
        if pd.Timestamp(end_exclusive) > pd.Timestamp(END_EXCLUSIVE):
            raise ValueError("R5 request crosses the sealed development boundary")
        raw = self._module.download(
            ticker, start=start, end=end_exclusive, interval="1d", auto_adjust=True,
            actions=True, threads=False, progress=False, timeout=20,
            multi_level_index=False,
        )
        frame = _normalize_download(raw)
        validate_price_frame_r3(frame, ticker)
        if pd.to_datetime(frame["date"]).max() >= pd.Timestamp(END_EXCLUSIVE):
            raise ValueError("R5 download crosses the sealed development boundary")
        return frame


def audit_r5_frames(prices):
    missing = sorted(set(R5_UNIVERSE).difference(prices))
    if missing:
        return {"passed": False, "missing": missing, "coverage": {}}
    for ticker in R5_UNIVERSE:
        validate_price_frame_r3(prices[ticker], ticker)
    spy_dates = set(pd.to_datetime(prices["SPY"]["date"]))
    coverage = {}
    for ticker in R5_UNIVERSE:
        dates = set(pd.to_datetime(prices[ticker]["date"]))
        coverage[ticker] = len(spy_dates & dates) / len(spy_dates) if spy_dates else 0.0
    latest = max(pd.to_datetime(frame["date"]).max() for frame in prices.values())
    earliest = {ticker: pd.to_datetime(prices[ticker]["date"]).min()
                for ticker in R5_UNIVERSE}
    passed = (
        bool(spy_dates)
        and min(coverage.values()) >= MIN_COMMON_CALENDAR_COVERAGE
        and latest < pd.Timestamp(END_EXCLUSIVE)
        and max(earliest.values()) <= pd.Timestamp(LATEST_ACCEPTABLE_FIRST_DATE)
    )
    return {
        "passed": passed, "missing": [], "coverage": coverage,
        "minimum_coverage": min(coverage.values()) if coverage else 0.0,
        "earliest_dates": {key: value.strftime("%Y-%m-%d") for key, value in earliest.items()},
        "latest_date": latest.strftime("%Y-%m-%d"),
    }


def build_r5_data_gate_snapshot(output_dir=DEFAULT_OUTPUT, source=None):
    source = source or R5YahooPriceSource()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prices, files = {}, {}
    for ticker in R5_UNIVERSE:
        frame = source.download(ticker)
        prices[ticker] = frame
        path = output_dir / f"{ticker}.csv"
        frame.to_csv(path, index=False, date_format="%Y-%m-%d")
        files[ticker] = {"file": path.name, "sha256": _sha256(path), "rows": len(frame)}
    audit = audit_r5_frames(prices)
    manifest = {
        "snapshot_id": "r5_000_2006_2014_data_gate_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": source.name, "source_version": source.version,
        "requested_start": START, "requested_end_exclusive": END_EXCLUSIVE,
        "evaluation_start": EVALUATION_START, "adjusted": True,
        "final_oos_downloaded": False, "universe": list(R5_UNIVERSE),
        "audit": audit, "files": files,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return load_r5_data_gate_snapshot(output_dir)


def load_r5_data_gate_snapshot(snapshot_dir=DEFAULT_OUTPUT):
    snapshot_dir = Path(snapshot_dir)
    manifest_path = snapshot_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("requested_end_exclusive") != END_EXCLUSIVE:
        raise ValueError("R5 manifest boundary mismatch")
    if manifest.get("final_oos_downloaded") is not False:
        raise ValueError("R5 manifest indicates Final OOS access")
    if tuple(manifest.get("universe", ())) != R5_UNIVERSE:
        raise ValueError("R5 manifest universe mismatch")
    prices = {}
    for ticker in R5_UNIVERSE:
        info = manifest["files"][ticker]
        path = snapshot_dir / info["file"]
        if _sha256(path) != info["sha256"]:
            raise ValueError(f"R5 snapshot hash mismatch: {ticker}")
        prices[ticker] = pd.read_csv(path, parse_dates=["date"])
    audit = audit_r5_frames(prices)
    if audit != manifest.get("audit") or not audit["passed"]:
        raise ValueError("R5 data-quality gate failed")
    return DataSnapshot(
        manifest["snapshot_id"], datetime.fromisoformat(manifest["created_at_utc"]),
        prices, universe=R5_UNIVERSE, source_name=manifest["provider"],
        metadata={"adjusted": True, "final_oos_downloaded": False,
                  "requested_start": START, "requested_end_exclusive": END_EXCLUSIVE,
                  "evaluation_start": EVALUATION_START,
                  "manifest_path": str(manifest_path.resolve()), "audit": audit},
    )


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
