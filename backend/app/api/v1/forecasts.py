from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ...deps import get_forecast_service
from ...domain.schemas import (
    ForecastCreate,
    ForecastRead,
    ForecastSummary,
    TargetCreate,
    TargetRead,
)
from ...domain.service import ForecastService

router = APIRouter(prefix="/v1", tags=["forecasts"])

ServiceDep = Annotated[ForecastService, Depends(get_forecast_service)]


@router.get("/health", summary="Liveness/health check")
def health(service: ServiceDep) -> dict[str, str]:
    return service.health()


# Targets

@router.post(
    "/targets",
    response_model=TargetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a forecast target",
)
def create_target(payload: TargetCreate, service: ServiceDep) -> TargetRead:
    return service.create_target(payload)


@router.get(
    "/targets",
    response_model=list[TargetRead],
    summary="List all forecast targets",
)
def list_targets(service: ServiceDep) -> list[TargetRead]:
    return service.list_targets()


@router.get(
    "/targets/{target_id}",
    response_model=TargetRead,
    summary="Get a single forecast target",
)
def get_target(target_id: UUID, service: ServiceDep) -> TargetRead:
    result = service.get_target(target_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")
    return result


# Forecasts

@router.post(
    "/forecasts",
    response_model=ForecastRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a forecast",
)
def create_forecast(payload: ForecastCreate, service: ServiceDep) -> ForecastRead:
    return service.create_forecast(payload)


@router.get(
    "/forecasts",
    response_model=list[ForecastRead],
    summary="List forecasts (optionally filtered by target)",
)
def list_forecasts(target_id: UUID | None = None, service: ServiceDep = Depends()) -> list[ForecastRead]:
    return service.list_forecasts(target_id=target_id)


@router.get(
    "/forecasts/{forecast_id}",
    response_model=ForecastRead,
    summary="Get a single forecast",
)
def get_forecast(forecast_id: UUID, service: ServiceDep) -> ForecastRead:
    result = service.get_forecast(forecast_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forecast not found")
    return result


@router.get(
    "/forecasts/summary",
    response_model=list[ForecastSummary],
    summary="Summarize forecasts by target",
)
def summarize_forecasts(service: ServiceDep) -> list[ForecastSummary]:
    return service.summarize_forecasts()
