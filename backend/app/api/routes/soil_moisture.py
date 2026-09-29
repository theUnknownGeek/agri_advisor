from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models import SoilMoisture
from app.schemas import (
    SoilMoistureCreate,
    SoilMoistureUpdate,
    SoilMoistureResponse
)


router = APIRouter(
    prefix="/soil_moisture",
    tags=["/soil_moisture"]
)


@router.get("/", response_model=List[SoilMoistureResponse])
def get_soil_moisture(db: Session = Depends(get_db)):

    records = db.query(SoilMoisture).all()

    return records



@router.post("/", response_model=SoilMoistureResponse)
def add_soil_moisture(
    moisture: SoilMoistureCreate,
    db: Session = Depends(get_db)
):

    new_record = SoilMoisture(
        field_id = moisture.field_id,
        moisture_percentage = moisture.moisture_percentage,
        recorded_at = moisture.recorded_at,
        source_soil = moisture.source_soil
    )


    db.add(new_record)

    db.commit()

    db.refresh(new_record)


    return new_record



@router.get("/{moisture_id}", response_model=SoilMoistureResponse)
def get_soil_record(
    moisture_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(SoilMoisture).filter(
        SoilMoisture.id == moisture_id
    ).first()


    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil moisture record not found"
        )


    return item




@router.put("/{moisture_id}", response_model=SoilMoistureResponse)
def update_soil_record(
    moisture_id: UUID,
    moisture: SoilMoistureUpdate,
    db: Session = Depends(get_db)
):

    item = db.query(SoilMoisture).filter(
        SoilMoisture.id == moisture_id
    ).first()


    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil moisture record not found"
        )


    if moisture.moisture_percentage is not None:
        item.moisture_percentage = moisture.moisture_percentage


    if moisture.recorded_at is not None:
        item.recorded_at = moisture.recorded_at


    if moisture.source_soil is not None:
        item.source_soil = moisture.source_soil


    db.commit()

    db.refresh(item)


    return item




@router.delete("/{moisture_id}")
def delete_soil_record(
    moisture_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(SoilMoisture).filter(
        SoilMoisture.id == moisture_id
    ).first()


    if item:

        db.delete(item)

        db.commit()

    else:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil moisture record not found"
        )


    return {
        "message": "Soil moisture record deleted successfully"
    }