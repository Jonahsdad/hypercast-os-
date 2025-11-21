from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Iterable
from uuid import UUID

from .entities import Forecast, ForecastTarget
from .repository import ForecastRepository
from .schemas import ForecastCreate, ForecastRead, ForecastSummary, TargetCreate, TargetRead


class ForecastService:
    """Application service layer for forecast operations."""

    def __init__(self, repository: ForecastRepository) -> None:
        self._repo = repository

    # Targets

    def create_target(self, payload: TargetCreate) -> TargetRead:
        target = ForecastTarget(
            name=payload.name,
            description=payload.description,
            horizon=payload.horizon,
        )
        saved = self._repo.create_target(target)
        return TargetRead(**asdict(saved))

    def list_targets(self) -> list[TargetRead]:
        targets = self._repo.list_targets()
        return [TargetRead(**asdict(t)) for t in targets]

    def get_target(self, target_id: UUID) -> TargetRead | None:
        target = self._repo.get_target(target_id)
        return TargetRead(**asdict(target)) if target else None

    # Forecasts

    def create_forecast(self, payload: ForecastCreate) -> ForecastRead:
        forecast = Forecast(
            target_id=payload.target_id,
            value=payload.value,
            probability=payload.probability,
            forecast_type=payload.forecast_type,
            model_name=payload.model_name,
            created_at=datetime.utcnow(),
        )
        saved = self._repo.create_forecast(forecast)
        return ForecastRead(**asdict(saved))

    def list_forecasts(self, target_id: UUID | None = None) -> list[ForecastRead]:
        forecasts = self._repo.list_forecasts(target_id)
        return [ForecastRead(**asdict(f)) for f in forecasts]

    def get_forecast(self, forecast_id: UUID) -> ForecastRead | None:
        forecast = self._repo.get_forecast(forecast_id)
        return ForecastRead(**asdict(forecast)) if forecast else None

    def summarize_forecasts(self) -> list[ForecastSummary]:
        groups = self._repo.aggregate_by_target()
        summaries: list[ForecastSummary] = []
        for target_id, forecasts in groups.items():
            if not forecasts:
                continue
            latest_ts = max(f.timestamp for f in forecasts)
            # Optional: could group by model as well.
            summaries.append(
                ForecastSummary(
                    target_id=target_id,
                    count=len(forecasts),
                    model_name=None,
                    latest_timestamp=latest_ts,
                )
            )
        return summaries

    def health(self) -> dict[str, str]:
        # Hook for future deeper checks
        return {"status": "ok", "time": datetime.utcnow().isoformat()}
