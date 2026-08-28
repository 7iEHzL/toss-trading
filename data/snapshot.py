from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Mapping, Optional, Protocol, Sequence

import pandas as pd


@dataclass(frozen=True)
class DataSnapshot:
    """Storage-neutral contract for one reproducible research snapshot."""

    snapshot_id: str
    as_of: datetime
    prices: Mapping[str, pd.DataFrame]
    fundamentals: Optional[Mapping[str, Any]] = None
    universe: Optional[Sequence[str]] = None
    source_name: str = "unspecified"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def provenance(self):
        return {
            "snapshot_id": self.snapshot_id,
            "as_of": self.as_of.isoformat(),
            "source_name": self.source_name,
            "universe_size": len(self.universe) if self.universe is not None else None,
            "metadata": dict(self.metadata),
        }


class DataSource(Protocol):
    """Minimal interface for future local, database, or object-store sources."""

    def load_snapshot(self, snapshot_id: str) -> DataSnapshot:
        ...
