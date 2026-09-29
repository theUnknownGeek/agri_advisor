from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Literal


class RecommendationResponse(BaseModel):

    id: UUID
    crop_cycle_id: UUID
    decision: Literal["IRRIGATE", "WAIT", "MONITOR"]
    reason: str
    confidence: Decimal
    status: Literal["ACTIVE","COMPLETED","DISMISSED"]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class RecommendationCreate(BaseModel):

    crop_cycle_id: UUID
    decision: Literal["IRRIGATE", "WAIT", "MONITOR"]
    reason: str
    confidence: Decimal
    status: Literal["ACTIVE","COMPLETED","DISMISSED"]

    model_config = {
        "from_attributes": True
    }


class RecommendationUpdate(BaseModel):

    decision: Literal["IRRIGATE", "WAIT", "MONITOR"] | None = None
    reason: str | None = None
    confidence: Decimal | None = None
    status: Literal["ACTIVE","COMPLETED","DISMISSED"] | None = None

    model_config = {
        "from_attributes": True
    }