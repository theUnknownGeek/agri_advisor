from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FarmerResponse(BaseModel):
    id:UUID
    name:str
    phone:str
    preferred_lang:str
    created_at:datetime

    model_config = {
        "from_attributes": True
    }

class FarmerCreate(BaseModel):
    name: str
    phone:str
    preferred_lang: str

    model_config = {
        "from_attributes": True
    }

class FarmerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    preferred_lang: str | None = None

    model_config={
        "from_attributes": True
    }