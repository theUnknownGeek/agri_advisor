from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import Farm
from typing import List
from app.schemas import FarmUpdate, FarmResponse,FarmCreate
from uuid import UUID
from decimal import Decimal

router = APIRouter(
    prefix="/farms",
    tags=["/farms"]
)

@router.get("/", response_model=List[FarmResponse])
def get_farms(db: Session = Depends(get_db)):
    farms = db.query(Farm).all()
    return farms

@router.post("/", response_model=FarmResponse)
def add_farms(
    farm: FarmCreate,
    db: Session = Depends(get_db)
):  
    new_farm = Farm(
        farmer_id = farm.farmer_id,
        name = farm.name,
        latitude = farm.latitude,
        longitude = farm.longitude,
        area = farm.area,
        area_unit = farm.area_unit 
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm_byID(farm_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Farm).filter(Farm.id == farm_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Farm not found"
        )

    return item

@router.put("/{farm_id}", response_model=FarmResponse)
def update_Farm(farm_id: UUID, farm: FarmUpdate, db:Session = Depends(get_db)):
    item = db.query(Farm).filter(Farm.id == farm_id).first()

    if item is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id not found"
        )

    if farm.name is not None:
            item.name = farm.name
    
    if farm.latitude is not None:
        item.latitude = farm.latitude
    
    if farm.longitude is not None:
        item.longitude = farm.longitude

    if farm.area is not None:
        item.area = farm.area

    if farm.area_unit is not None:
        item.area_unit = farm.area_unit

    db.commit()
    db.refresh(item)

    return item

@router.delete("/{farm_id}")
def del_farm(farm_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Farm).filter(Farm.id == farm_id).first()

    if item:
        db.delete(item)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id not found"
        )

    return {"message": f"Farm with the given i deleted successfully"}