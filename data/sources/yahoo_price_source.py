"""Yahoo price adapter restricted to the sealed R3 development interval."""

from dataclasses import dataclass
import time

import pandas as pd

from data.r3_validator import validate_price_frame_r3
from data.yfinance_source import _normalize_download


R3_START = "2014-07-01"
R3_END_EXCLUSIVE = "2023-01-01"


@dataclass(frozen=True)
class DownloadFailure:
    ticker: str
    category: str
    message: str
    attempts: int
    retryable: bool


class YahooPriceSource:
    name = "Yahoo Finance via yfinance"

    def __init__(self, module=None, auto_adjust=True):
        if module is None:
            import yfinance as module
        self._module = module
        self.auto_adjust = bool(auto_adjust)
        self.last_recovered = set()

    @property
    def version(self):
        return getattr(self._module, "__version__", "unknown")

    def download(self, ticker, start=R3_START, end_exclusive=R3_END_EXCLUSIVE):
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end_exclusive)
        if start_ts < pd.Timestamp(R3_START) or end_ts > pd.Timestamp(R3_END_EXCLUSIVE):
            raise ValueError("price request violates the Final OOS seal")
        if end_ts <= start_ts:
            raise ValueError("price end must be after start")
        raw = self._module.download(
            ticker, start=start_ts.strftime("%Y-%m-%d"),
            end=end_ts.strftime("%Y-%m-%d"), interval="1d",
            auto_adjust=self.auto_adjust, actions=True, threads=False,
            progress=False, timeout=20, multi_level_index=False,
        )
        frame = _normalize_download(raw)
        validate_price_frame_r3(frame, ticker)
        if pd.to_datetime(frame["date"]).max() >= pd.Timestamp(R3_END_EXCLUSIVE):
            raise ValueError("download contains Final OOS data")
        return frame

    def download_many(self, tickers, start=R3_START,
                      end_exclusive=R3_END_EXCLUSIVE, chunk_size=25,
                      max_attempts=2, retry_delay_seconds=1.0):
        """Batch-download prices and retry batch misses individually.

        A failed Yahoo lookup is never labelled delisted automatically. Delisting,
        merger and rename states require separate identity/corporate-action evidence.
        """
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end_exclusive)
        if start_ts < pd.Timestamp(R3_START) or end_ts > pd.Timestamp(R3_END_EXCLUSIVE):
            raise ValueError("price request violates the Final OOS seal")
        symbols = list(dict.fromkeys(tickers))
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        frames, failures = {}, {}
        self.last_recovered = set()
        for offset in range(0, len(symbols), chunk_size):
            chunk = symbols[offset:offset + chunk_size]
            raw = self._module.download(
                chunk, start=start_ts.strftime("%Y-%m-%d"),
                end=end_ts.strftime("%Y-%m-%d"), interval="1d",
                auto_adjust=self.auto_adjust, actions=True, threads=True,
                progress=False, timeout=20, group_by="ticker",
            )
            for symbol in chunk:
                try:
                    selected = raw[symbol] if isinstance(raw.columns, pd.MultiIndex) else raw
                    frame = _normalize_download(selected.dropna(how="all"))
                    validate_price_frame_r3(frame, symbol)
                    if pd.to_datetime(frame["date"]).max() >= pd.Timestamp(R3_END_EXCLUSIVE):
                        raise ValueError("download contains Final OOS data")
                    frames[symbol] = frame
                except (KeyError, ValueError) as exc:
                    failures[symbol] = DownloadFailure(
                        symbol, _classify_download_error(exc), str(exc), 1, True
                    )

        for symbol in list(failures):
            last_error = failures[symbol]
            for attempt in range(2, max_attempts + 1):
                delay = _retry_delay(retry_delay_seconds, attempt)
                if delay:
                    time.sleep(delay)
                try:
                    frames[symbol] = self.download(symbol, start, end_exclusive)
                    self.last_recovered.add(symbol)
                    failures.pop(symbol, None)
                    break
                except (KeyError, ValueError, RuntimeError) as exc:
                    category = _classify_download_error(exc)
                    last_error = DownloadFailure(
                        symbol, category, str(exc), attempt,
                        category in {"temporary_api_failure", "rate_limited", "timeout",
                                     "unknown_download_failure"},
                    )
            else:
                failures[symbol] = last_error
        return frames, failures


def _classify_download_error(error):
    message = str(error).lower()
    if "rate limit" in message or "too many requests" in message:
        return "rate_limited"
    if "timeout" in message or "timed out" in message:
        return "timeout"
    if any(token in message for token in (
            "connection", "crumb", "json", "temporarily")):
        return "temporary_api_failure"
    if "final oos" in message or "sealed" in message:
        return "safety_boundary_failure"
    if "no data" in message or "empty" in message or "returned no data" in message:
        return "price_not_returned"
    if "missing columns" in message or "inconsistent" in message:
        return "invalid_price_payload"
    return "unknown_download_failure"


def _retry_delay(value, attempt):
    if isinstance(value, (tuple, list)):
        index = min(attempt - 2, len(value) - 1)
        return value[index] if value else 0
    return value
