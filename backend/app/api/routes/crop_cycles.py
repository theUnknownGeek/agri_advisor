from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import Crop_cycles
from typing import List
from app.schemas import CCUpdate, CCResponse,CCCreate
from uuid import UUID
from decimal import Decimal

router = APIRouter(
    prefix="/crop_cycles",
    tags=["/crop_cycles"]
)

@router.get("/", response_model=List[CCResponse])
def get_crop_cycles(db: Session = Depends(get_db)):
    cropCycle = db.query(Crop_cycles).all()
    return cropCycle

@router.post("/", response_model=CCResponse)
def add_crop(
    cropCycle: CCCreate,
    db: Session = Depends(get_db)
):  
    new_crop = Crop_cycles(
        field_id = cropCycle.field_id,
        crop = cropCycle.crop,
        variety = cropCycle.variety,
        season = cropCycle.season,
        planting_date = cropCycle.planting_date,
        establishment_method = cropCycle.establishment_method,
        current_growth_stage = cropCycle.current_growth_stage
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    return new_crop

@router.get("/{Crop_cycles_id}", response_model=CCResponse)
def get_cropCycle_byID(Crop_cycles_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Crop_cycles).filter(Crop_cycles.id == Crop_cycles_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Field not found"
        )

    return item

@router.put("/{Crop_cycles_id}", response_model=CCResponse)
def update_cropCycle(Crop_cycles_id: UUID, cropCycle: CCUpdate, db:Session = Depends(get_db)):
    item = db.query(Crop_cycles).filter(Crop_cycles.id == Crop_cycles_id).first()

    if item is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id not found"
        )

    if cropCycle.crop is not None:
            item.crop = cropCycle.crop

    if cropCycle.variety is not None:
        item.variety = cropCycle.variety

    if cropCycle.season is not None:
        item.season = cropCycle.season

    if cropCycle.planting_date is not None:
        item.planting_date = cropCycle.planting_date

    if cropCycle.establishment_method is not None:
        item.establishment_method = cropCycle.establishment_method

    if cropCycle.current_growth_stage is not None:
        item.current_growth_stage = cropCycle.current_growth_stage

    db.commit()
    db.refresh(item)

    return item

@router.delete("/{Crop_cycles_id}")
def del_cropCycle(Crop_cycles_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Crop_cycles).filter(Crop_cycles.id == Crop_cycles_id).first()

    if item:
        db.delete(item)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id not found"
        )

    return {"message": f"Field with the given id deleted successfully"}