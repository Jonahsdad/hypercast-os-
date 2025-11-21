from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


ForecastType = Literal["point", "probability"]


class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    horizon: int = Field(1, ge=1, le=365)


class TargetRead(BaseModel):
    id: UUID
    name: str
    description: str
    horizon: int
    created_at: datetime


class ForecastCreate(BaseModel):
    target_id: UUID | None = None
    value: float | None = None
    probability: float | None = None
    forecast_type: ForecastType = "point"
    model_name: str = Field("manual", min_length=1, max_length=100)

    @field_validator("probability")
    @classmethod
    def validate_probability(cls, v: float | None, info):  # type: ignore[override]
        # Only validate when probability is present
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("probability must be between 0 and 1")
        return v

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: float | None):  # type: ignore[override]
        return v


class ForecastRead(BaseModel):
    id: UUID
    target_id: UUID | None
    timestamp: datetime
    value: float | None
    probability: float | None
    forecast_type: ForecastType
    model_name: str
    created_at: datetime


class ForecastSummary(BaseModel):
    target_id: UUID | None
    count: int
    model_name: str | None = None
    latest_timestamp: datetime | None = None
