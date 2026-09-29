from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal



class WeatherDataResponse(BaseModel):

    id: UUID
    field_id: UUID
    timestamp: datetime

    temperature: Decimal
    humidity: Decimal
    rainfall: Decimal
    rain_probability: Decimal

    wind_speed: Decimal | None

    data_type: str

    created_at: datetime


    model_config = {
        "from_attributes": True
    }



class WeatherDataCreate(BaseModel):

    field_id: UUID
    timestamp: datetime

    temperature: Decimal
    humidity: Decimal
    rainfall: Decimal
    rain_probability: Decimal

    wind_speed: Decimal | None = None

    data_type: str


    model_config = {
        "from_attributes": True
    }



class WeatherDataUpdate(BaseModel):

    timestamp: datetime | None = None

    temperature: Decimal | None = None
    humidity: Decimal | None = None
    rainfall: Decimal | None = None
    rain_probability: Decimal | None = None

    wind_speed: Decimal | None = None

    data_type: str | None = None


    model_config = {
        "from_attributes": True
    }