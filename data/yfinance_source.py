import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from data.snapshot import DataSnapshot


R1_SYMBOLS = ("AMD", "TSLA", "AMZN", "AAPL", "SPXL", "SPY")
R1_START = "2015-01-01"
R1_END_EXCLUSIVE = "2023-01-01"
REQUIRED_COLUMNS = ("date", "open", "high", "low", "close", "volume")


def download_r1_development_snapshot(output_dir):
    """Download and freeze only the R1 development interval from Yahoo."""
    import yfinance as yf

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    frames = {}

    for symbol in R1_SYMBOLS:
        raw = yf.download(
            symbol,
            start=R1_START,
            end=R1_END_EXCLUSIVE,
            interval="1d",
            auto_adjust=True,
            actions=True,
            threads=False,
            progress=False,
            timeout=20,
            multi_level_index=False,
        )
        frame = _normalize_download(raw)
        validate_price_frame(frame, symbol)
        path = output_dir / f"{symbol}.csv"
        frame.to_csv(path, index=False, date_format="%Y-%m-%d")
        files[symbol] = {
            "file": path.name,
            "sha256": _sha256(path),
            "rows": len(frame),
            "first_date": frame["date"].iloc[0].strftime("%Y-%m-%d"),
            "last_date": frame["date"].iloc[-1].strftime("%Y-%m-%d"),
        }
        frames[symbol] = frame

    common_dates = set.intersection(
        *(set(frame["date"]) for frame in frames.values())
    )
    if len(common_dates) < 126 + 2:
        raise ValueError("insufficient common trading dates for R1 warm-up")

    manifest = {
        "snapshot_id": f"r1-yfinance-dev-{R1_START}-{R1_END_EXCLUSIVE}",
        "provider": "Yahoo Finance via yfinance",
        "source_library": "yfinance",
        "source_library_version": yf.__version__,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_start": R1_START,
        "requested_end_exclusive": R1_END_EXCLUSIVE,
        "adjusted": True,
        "auto_adjust": True,
        "actions": True,
        "final_oos_downloaded": False,
        "symbols": list(R1_SYMBOLS),
        "common_trading_dates": len(common_dates),
        "files": files,
        "warnings": [
            "Yahoo/yfinance data is suitable for research baseline use but is not institutional-grade.",
            "The R1 universe is ex-post selected and may contain selection or survivorship bias.",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return load_r1_development_snapshot(output_dir)


def load_r1_development_snapshot(snapshot_dir):
    snapshot_dir = Path(snapshot_dir)
    manifest_path = snapshot_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _validate_manifest(manifest)

    prices = {}
    for symbol in R1_SYMBOLS:
        file_info = manifest["files"][symbol]
        path = snapshot_dir / file_info["file"]
        if _sha256(path) != file_info["sha256"]:
            raise ValueError(f"snapshot hash mismatch: {symbol}")
        frame = pd.read_csv(path, parse_dates=["date"])
        validate_price_frame(frame, symbol)
        prices[symbol] = frame

    return DataSnapshot(
        snapshot_id=manifest["snapshot_id"],
        as_of=datetime.fromisoformat(manifest["downloaded_at_utc"]),
        prices=prices,
        universe=manifest["symbols"],
        source_name=manifest["provider"],
        metadata={
            "adjusted": True,
            "requested_start": manifest["requested_start"],
            "requested_end_exclusive": manifest["requested_end_exclusive"],
            "source_library_version": manifest["source_library_version"],
            "final_oos_downloaded": False,
            "manifest_path": str(manifest_path.resolve()),
            "warnings": manifest["warnings"],
        },
    )


def validate_price_frame(frame, symbol="unknown"):
    missing = set(REQUIRED_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError(f"{symbol} missing columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError(f"{symbol} has no observations")

    dates = pd.to_datetime(frame["date"], errors="coerce")
    if dates.isna().any() or dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError(f"{symbol} dates must be valid, unique, and sorted")
    if dates.min() < pd.Timestamp(R1_START) or dates.max() >= pd.Timestamp(R1_END_EXCLUSIVE):
        raise ValueError(f"{symbol} contains data outside the sealed development request")

    for column in ("open", "high", "low", "close"):
        values = pd.to_numeric(frame[column], errors="coerce")
        if values.isna().any() or not values.map(math.isfinite).all() or (values <= 0).any():
            raise ValueError(f"{symbol} {column} must contain finite positive prices")
    volume = pd.to_numeric(frame["volume"], errors="coerce")
    if volume.isna().any() or not volume.map(math.isfinite).all() or (volume < 0).any():
        raise ValueError(f"{symbol} volume must be finite and non-negative")
    tolerance = 1e-10
    if (frame["high"] + tolerance < frame[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError(f"{symbol} high is inconsistent with OHLC")
    if (frame["low"] - tolerance > frame[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError(f"{symbol} low is inconsistent with OHLC")


def _normalize_download(raw):
    if raw is None or raw.empty:
        raise ValueError("yfinance returned no data")
    frame = raw.reset_index()
    frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
    frame = frame.rename(columns={"datetime": "date"})
    keep = [column for column in (
        "date", "open", "high", "low", "close", "volume", "dividends", "stock_splits"
    ) if column in frame.columns]
    frame = frame[keep].copy()
    frame["date"] = pd.to_datetime(frame["date"]).dt.tz_localize(None)
    return frame.sort_values("date").reset_index(drop=True)


def _validate_manifest(manifest):
    if manifest.get("requested_end_exclusive") != R1_END_EXCLUSIVE:
        raise ValueError("manifest does not preserve the R1 final-OOS seal")
    if manifest.get("final_oos_downloaded") is not False:
        raise ValueError("manifest indicates final OOS was downloaded")
    if manifest.get("adjusted") is not True:
        raise ValueError("manifest is not adjusted")
    if set(manifest.get("symbols", [])) != set(R1_SYMBOLS):
        raise ValueError("manifest symbol set does not match R1")


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
