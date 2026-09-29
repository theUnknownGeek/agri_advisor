from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlalchemy import DECIMAL, Column
from sqlalchemy.orm import declarative_base
from decimal import Decimal
from datetime import date, datetime

class CCResponse(BaseModel):
    id:UUID
    field_id: UUID
    crop:str
    variety:str
    season: str
    planting_date: date
    establishment_method: str
    current_growth_stage: str
    created_at:datetime

    model_config = {
            "from_attributes": True
    }

class CCCreate(BaseModel):
    field_id: UUID
    crop:str
    variety:str
    season: str
    planting_date: date
    establishment_method: str
    current_growth_stage: str

    model_config = {
            "from_attributes": True
    }

class CCUpdate(BaseModel):
    crop: str | None = None
    variety: str | None = None
    season: str | None = None
    planting_date: date | None = None
    establishment_method: str | None = None
    current_growth_rate: str | None = None

    model_config = {
            "from_attributes": True
    }