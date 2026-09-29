from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlalchemy import DECIMAL, Column
from sqlalchemy.orm import declarative_base
from decimal import Decimal
class FarmResponse(BaseModel):
    id:UUID
    farmer_id: UUID
    name:str
    latitude:Decimal
    longitude:Decimal
    area:Decimal
    area_unit: str
    created_at:datetime

    model_config = {
            "from_attributes": True
    }

class FarmCreate(BaseModel):
    farmer_id: UUID
    name: str
    latitude: Decimal
    longitude: Decimal
    area: Decimal
    area_unit: str

    model_config = {
            "from_attributes": True
    }

class FarmUpdate(BaseModel):
    name: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    area: Decimal | None = None
    area_unit: str | None = None

    model_config = {
            "from_attributes": True
    }