from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from threading import RLock
from typing import Iterable
from uuid import UUID

from .entities import Forecast, ForecastTarget


class ForecastRepository(ABC):
    """Abstract repository interface."""

    @abstractmethod
    def create_target(self, target: ForecastTarget) -> ForecastTarget: ...

    @abstractmethod
    def list_targets(self) -> list[ForecastTarget]: ...

    @abstractmethod
    def get_target(self, target_id: UUID) -> ForecastTarget | None: ...

    @abstractmethod
    def create_forecast(self, forecast: Forecast) -> Forecast: ...

    @abstractmethod
    def list_forecasts(self, target_id: UUID | None = None) -> list[Forecast]: ...

    @abstractmethod
    def get_forecast(self, forecast_id: UUID) -> Forecast | None: ...

    @abstractmethod
    def list_all_forecasts(self) -> Iterable[Forecast]: ...


class InMemoryForecastRepository(ForecastRepository):
    """Thread-safe in-memory implementation for rapid prototyping and tests."""

    def __init__(self) -> None:
        self._targets: dict[UUID, ForecastTarget] = {}
        self._forecasts: dict[UUID, Forecast] = {}
        self._lock = RLock()

    def create_target(self, target: ForecastTarget) -> ForecastTarget:
        with self._lock:
            self._targets[target.id] = target
        return target

    def list_targets(self) -> list[ForecastTarget]:
        with self._lock:
            return list(self._targets.values())

    def get_target(self, target_id: UUID) -> ForecastTarget | None:
        with self._lock:
            return self._targets.get(target_id)

    def create_forecast(self, forecast: Forecast) -> Forecast:
        if forecast.created_at is None:
            forecast.created_at = datetime.utcnow()
        with self._lock:
            self._forecasts[forecast.id] = forecast
        return forecast

    def list_forecasts(self, target_id: UUID | None = None) -> list[Forecast]:
        with self._lock:
            if target_id is None:
                return list(self._forecasts.values())
            return [f for f in self._forecasts.values() if f.target_id == target_id]

    def get_forecast(self, forecast_id: UUID) -> Forecast | None:
        with self._lock:
            return self._forecasts.get(forecast_id)

    def list_all_forecasts(self) -> Iterable[Forecast]:
        with self._lock:
            return list(self._forecasts.values())

    def aggregate_by_target(self) -> dict[UUID | None, list[Forecast]]:
        grouped: dict[UUID | None, list[Forecast]] = defaultdict(list)
        with self._lock:
            for f in self._forecasts.values():
                grouped[f.target_id].append(f)
        return grouped
