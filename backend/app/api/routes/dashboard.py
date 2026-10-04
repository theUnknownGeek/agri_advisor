from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db

from app.models import (
    Crop_cycles,
    Field,
    SoilMoisture,
    WeatherData,
    Recommendation
)


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)



@router.get("/{crop_cycle_id}")
def get_dashboard(
    crop_cycle_id: UUID,
    db: Session = Depends(get_db)
):

    crop_cycle = db.query(Crop_cycles)\
        .filter(
            Crop_cycles.id == crop_cycle_id
        )\
        .first()


    if not crop_cycle:
        raise HTTPException(
            status_code=404,
            detail="Crop cycle not found"
        )


    field = db.query(Field)\
        .filter(
            Field.id == crop_cycle.field_id
        )\
        .first()



    soil = db.query(SoilMoisture)\
        .filter(
            SoilMoisture.field_id == field.id
        )\
        .order_by(
            SoilMoisture.recorded_at.desc()
        )\
        .first()



    weather = db.query(WeatherData)\
        .filter(
            WeatherData.field_id == field.id
        )\
        .order_by(
            WeatherData.timestamp.desc()
        )\
        .first()



    recommendation = db.query(Recommendation)\
        .filter(
            Recommendation.crop_cycle_id == crop_cycle_id
        )\
        .order_by(
            Recommendation.created_at.desc()
        )\
        .first()



    return {

        "crop": crop_cycle.crop,


        "field":{
            "id":str(field.id),
            "area":field.area,
        },


        "soil":{
            "moisture":soil.moisture_percentage if soil else None
        },


        "weather":{
            "temperature":weather.temperature if weather else None,
            "humidity":weather.humidity if weather else None,
            "rain_probability":weather.rain_probability if weather else None
        },


        "recommendation":{

            "decision":recommendation.decision if recommendation else None,
            "reason":recommendation.reason if recommendation else None,
            "confidence":float(recommendation.confidence) if recommendation else None,
            "status":recommendation.status if recommendation else None

        }

    }