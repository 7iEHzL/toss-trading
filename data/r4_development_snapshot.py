"""Immutable development snapshot for R4A; Final OOS is structurally excluded."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from data.snapshot import DataSnapshot
from data.r3_validator import validate_price_frame_r3
from data.sources.yahoo_price_source import YahooPriceSource


R4A_UNIVERSE = ("SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "IYR", "GLD", "DBC")
START = "2014-07-01"
END_EXCLUSIVE = "2023-01-01"
DEFAULT_OUTPUT = Path("data/snapshots/r4/r4a_development_2014_2022_v1")


def build_r4a_development_snapshot(output_dir=DEFAULT_OUTPUT, source=None):
    source = source or YahooPriceSource()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    for ticker in R4A_UNIVERSE:
        frame = source.download(ticker, START, END_EXCLUSIVE)
        path = output_dir / f"{ticker}.csv"
        frame.to_csv(path, index=False, date_format="%Y-%m-%d")
        files[ticker] = {
            "file": path.name, "sha256": _sha256(path), "rows": len(frame),
            "first_date": frame["date"].iloc[0].strftime("%Y-%m-%d"),
            "last_date": frame["date"].iloc[-1].strftime("%Y-%m-%d"),
        }
    manifest = {
        "snapshot_id": "r4a_development_2014_2022_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "Yahoo Finance via yfinance",
        "source_version": source.version,
        "requested_start": START, "requested_end_exclusive": END_EXCLUSIVE,
        "adjusted": True, "final_oos_downloaded": False,
        "universe": list(R4A_UNIVERSE), "files": files,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return load_r4a_development_snapshot(output_dir)


def load_r4a_development_snapshot(snapshot_dir=DEFAULT_OUTPUT):
    snapshot_dir = Path(snapshot_dir)
    manifest = json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("requested_end_exclusive") != END_EXCLUSIVE:
        raise ValueError("R4A manifest violates Final OOS seal")
    if manifest.get("final_oos_downloaded") is not False:
        raise ValueError("R4A manifest indicates Final OOS access")
    if tuple(manifest.get("universe", ())) != R4A_UNIVERSE:
        raise ValueError("R4A manifest universe mismatch")
    prices = {}
    for ticker in R4A_UNIVERSE:
        info = manifest["files"][ticker]
        path = snapshot_dir / info["file"]
        if _sha256(path) != info["sha256"]:
            raise ValueError(f"R4A snapshot hash mismatch: {ticker}")
        frame = pd.read_csv(path, parse_dates=["date"])
        validate_price_frame_r3(frame, ticker)
        prices[ticker] = frame
    return DataSnapshot(
        manifest["snapshot_id"], datetime.fromisoformat(manifest["created_at_utc"]),
        prices, universe=R4A_UNIVERSE, source_name=manifest["provider"],
        metadata={"adjusted": True, "final_oos_downloaded": False,
                  "requested_start": START, "requested_end_exclusive": END_EXCLUSIVE,
                  "manifest_path": str((snapshot_dir / "manifest.json").resolve())},
    )


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
