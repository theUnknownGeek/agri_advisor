from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID


from app.db.database import get_db
from app.models import Recommendation, Crop_cycles, Field, SoilMoisture, Farm, IrrigationLog, soil_moisture, WeatherData
from app.schemas import (
    RecommendationCreate,
    RecommendationResponse,
    RecommendationUpdate
)
from app.services.recommendation_service import create_recommendation


router = APIRouter(
    prefix="/recommendations",
    tags=["/recommendations"]
)


# GET ALL

@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(
    db: Session = Depends(get_db)
):

    recommendations = db.query(Recommendation).all()

    return recommendations



# CREATE

@router.post("/", response_model=RecommendationResponse)
def add_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):

    new_recommendation = Recommendation(

        crop_cycle_id = recommendation.crop_cycle_id,
        decision = recommendation.decision,
        reason = recommendation.reason,
        confidence = recommendation.confidence,
        status = recommendation.status

    )


    db.add(new_recommendation)

    db.commit()

    db.refresh(new_recommendation)


    return new_recommendation



# GET BY ID

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def get_recommendation_by_id(
    recommendation_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(Recommendation)\
        .filter(Recommendation.id == recommendation_id)\
        .first()


    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )


    return item




# UPDATE

@router.put("/{recommendation_id}", response_model=RecommendationResponse)
def update_recommendation(
    recommendation_id: UUID,
    recommendation: RecommendationUpdate,
    db: Session = Depends(get_db)
):

    item = db.query(Recommendation)\
        .filter(Recommendation.id == recommendation_id)\
        .first()


    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )


    if recommendation.decision is not None:
        item.decision = recommendation.decision


    if recommendation.reason is not None:
        item.reason = recommendation.reason


    if recommendation.confidence is not None:
        item.confidence = recommendation.confidence


    if recommendation.status is not None:
        item.status = recommendation.status



    db.commit()

    db.refresh(item)


    return item




# DELETE

@router.delete("/{recommendation_id}")
def delete_recommendation(
    recommendation_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(Recommendation)\
        .filter(Recommendation.id == recommendation_id)\
        .first()


    if item:

        db.delete(item)

        db.commit()


    else:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )


    return {
        "message": "Recommendation deleted successfully"
    }

@router.post("/generate/{crop_cycle_id}", response_model=RecommendationResponse)
def generate(crop_cycle_id: UUID, db:Session = Depends(get_db)):
    crop_cycle = db.query(Crop_cycles).filter(Crop_cycles.id==crop_cycle_id).first()

    if crop_cycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop cycle not found"
        )

    field = db.query(Field).filter(Field.id==crop_cycle.field_id).first()

    if field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    soil = db.query(SoilMoisture).filter(SoilMoisture.field_id == field.id).order_by(SoilMoisture.recorded_at.desc()).first()

    if soil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil Data not found"
        )

    weather = db.query(WeatherData).filter(WeatherData.field_id==field.id).order_by(WeatherData.timestamp.desc()).first()

    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather Data not found"
        )

    soil_moisture = soil.moisture_percentage
    rain_probability = weather.rain_probability

    recommendation = create_recommendation(
        db,
        soil_moisture,
        rain_probability,
        crop_cycle_id
    )

    return recommendation
