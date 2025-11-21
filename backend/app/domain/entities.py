from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4


ForecastType = Literal["point", "probability"]


@dataclass(slots=True)
class ForecastTarget:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    horizon: int = 1  # steps ahead
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class Forecast:
    id: UUID = field(default_factory=uuid4)
    target_id: UUID | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    value: float | None = None
    probability: float | None = None
    forecast_type: ForecastType = "point"
    model_name: str = "unknown"
    created_at: datetime = field(default_factory=datetime.utcnow)
