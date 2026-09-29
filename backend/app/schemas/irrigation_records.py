from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal


class IrrigationLogResponse(BaseModel):
    id: UUID
    field_id: UUID
    irrigation_date: date
    duration_minutes: int
    irrigation_amount: Decimal
    amount_unit: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class IrrigationLogCreate(BaseModel):
    field_id: UUID
    irrigation_date: date
    duration_minutes: int
    irrigation_amount: Decimal
    amount_unit: str

    model_config = {
        "from_attributes": True
    }


class IrrigationLogUpdate(BaseModel):
    irrigation_date: date | None = None
    duration_minutes: int | None = None
    irrigation_amount: Decimal | None = None
    amount_unit: str | None = None

    model_config = {
        "from_attributes": True
    }