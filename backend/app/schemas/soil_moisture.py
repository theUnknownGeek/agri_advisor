from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class SoilMoistureResponse(BaseModel):

    id: UUID
    field_id: UUID
    moisture_percentage: Decimal
    recorded_at: datetime
    source_soil: str
    created_at: datetime


    model_config = {
        "from_attributes": True
    }


class SoilMoistureCreate(BaseModel):

    field_id: UUID
    moisture_percentage: Decimal
    recorded_at: datetime
    source_soil: str


    model_config = {
        "from_attributes": True
    }


class SoilMoistureUpdate(BaseModel):

    moisture_percentage: Decimal | None = None
    recorded_at: datetime | None = None
    source_soil: str | None = None


    model_config = {
        "from_attributes": True
    }