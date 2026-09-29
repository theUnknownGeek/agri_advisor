from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlalchemy import DECIMAL, Column
from sqlalchemy.orm import declarative_base
from decimal import Decimal

class FieldResponse(BaseModel):
    id:UUID
    farm_id: UUID
    name:str
    area:Decimal
    area_unit: str
    soil_type: str
    created_at:datetime

    model_config = {
            "from_attributes": True
    }

class FieldCreate(BaseModel):
    farm_id: UUID
    name: str
    area: Decimal
    area_unit: str
    soil_type: str

    model_config = {
            "from_attributes": True
    }

class FieldUpdate(BaseModel):
    name: str | None = None
    area: Decimal | None = None
    area_unit: str | None = None
    soil_type: str | None = None

    model_config = {
            "from_attributes": True
    }