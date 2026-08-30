"""Point-in-time index membership adapter with no runtime refresh."""

from dataclasses import dataclass

import pandas as pd


R3_START = pd.Timestamp("2014-07-01")
R3_END_EXCLUSIVE = pd.Timestamp("2023-01-01")


@dataclass(frozen=True)
class MembershipRecord:
    as_of: pd.Timestamp
    ticker: str
    source: str
    status: str = "member"


class PitIndexMembershipSource:
    name = "pitindex"

    def __init__(self, module=None):
        if module is None:
            try:
                import pitindex as module
            except ImportError as exc:
                raise RuntimeError("pitindex is required for R3 membership") from exc
        self._module = module

    def info(self):
        return dict(self._module.info(index="sp500"))

    def constituents(self, as_of):
        date = _validate_development_date(as_of)
        raw = self._module.get_constituents(date.strftime("%Y-%m-%d"), index="sp500")
        return _normalize(raw, date)

    def history(self, start=R3_START, end_exclusive=R3_END_EXCLUSIVE):
        start = _validate_development_date(start)
        end = pd.Timestamp(end_exclusive).normalize()
        if end > R3_END_EXCLUSIVE or end <= start:
            raise ValueError("membership range violates the Final OOS seal")
        raw = self._module.get_constituents_history(
            start.strftime("%Y-%m-%d"),
            (end - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            index="sp500",
        )
        if raw is None or raw.empty:
            raise ValueError("pitindex returned no membership history")
        frames = []
        for as_of, frame in raw.groupby("as_of", sort=True):
            frames.append(_normalize(frame, pd.Timestamp(as_of).normalize()))
        return pd.concat(frames, ignore_index=True)


def _validate_development_date(value):
    date = pd.Timestamp(value).normalize()
    if date < R3_START or date >= R3_END_EXCLUSIVE:
        raise ValueError("membership request violates the Final OOS seal")
    return date


def _normalize(raw, as_of):
    if raw is None or raw.empty or "ticker" not in raw.columns:
        raise ValueError("membership response is empty or missing ticker")
    frame = raw.copy()
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    if frame["ticker"].eq("").any() or frame["ticker"].duplicated().any():
        raise ValueError("membership tickers must be non-empty and unique")
    frame["as_of"] = as_of
    frame["membership_status"] = "member"
    frame["membership_source"] = "pitindex"
    columns = ["as_of", "ticker", "membership_status", "membership_source"]
    columns += [c for c in ("name", "cik", "gics_sector", "gics_sub_industry") if c in frame]
    return frame[columns].sort_values("ticker").reset_index(drop=True)
