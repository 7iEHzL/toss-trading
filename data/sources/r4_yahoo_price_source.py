"""Yahoo adapter restricted to the R4-000 pre-freeze audit interval."""

import pandas as pd

from data.r4_validator import AUDIT_START, FREEZE_END_EXCLUSIVE, validate_r4_price_frame


class R4YahooPriceSource:
    def __init__(self, module=None):
        if module is None:
            import yfinance as module
        self._module = module

    @property
    def version(self):
        return getattr(self._module, "__version__", "unknown")

    def download(self, ticker, start=AUDIT_START, end_exclusive=FREEZE_END_EXCLUSIVE):
        start = pd.Timestamp(start)
        end_exclusive = pd.Timestamp(end_exclusive)
        if start != AUDIT_START or end_exclusive != FREEZE_END_EXCLUSIVE:
            raise ValueError("R4-000 source only permits the pre-registered audit interval")
        raw = self._module.download(
            ticker, start=start.strftime("%Y-%m-%d"),
            end=end_exclusive.strftime("%Y-%m-%d"), interval="1d",
            auto_adjust=False, actions=True, threads=False, progress=False,
            timeout=20, multi_level_index=False,
        )
        frame = normalize_r4_download(raw)
        validate_r4_price_frame(frame, ticker)
        return frame


def normalize_r4_download(raw):
    if raw is None or raw.empty:
        raise ValueError("yfinance returned no data")
    frame = raw.reset_index()
    frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
    frame = frame.rename(columns={"datetime": "date", "adj_close": "adjusted_close"})
    required = {"date", "open", "high", "low", "close", "adjusted_close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"yfinance missing columns: {', '.join(sorted(missing))}")
    raw_close = pd.to_numeric(frame["close"], errors="coerce")
    factor = pd.to_numeric(frame["adjusted_close"], errors="coerce") / raw_close
    result = pd.DataFrame({
        "date": pd.to_datetime(frame["date"]).dt.tz_localize(None),
        "open": pd.to_numeric(frame["open"], errors="coerce") * factor,
        "high": pd.to_numeric(frame["high"], errors="coerce") * factor,
        "low": pd.to_numeric(frame["low"], errors="coerce") * factor,
        "close": pd.to_numeric(frame["adjusted_close"], errors="coerce"),
        "raw_close": raw_close,
        "volume": pd.to_numeric(frame["volume"], errors="coerce"),
    })
    return result.sort_values("date").reset_index(drop=True)
