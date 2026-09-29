from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import Farmer
from typing import List
from app.schemas import FarmerResponse, FarmerUpdate,FarmerCreate
from uuid import UUID

router  = APIRouter(
    prefix="/farmers",
    tags=["/farmers"]
)

@router.get("/", response_model=List[FarmerResponse])
def get_farmers(db:Session = Depends(get_db)):
    farmers = db.query(Farmer).all()
    return farmers

@router.post("/", response_model=FarmerResponse)
def add_farmers(
    farmer: FarmerCreate,
    db:Session = Depends(get_db)
):
    new_farmer = Farmer(
        name = farmer.name,
        phone = farmer.phone,
        preferred_lang = farmer.preferred_lang
    )

    db.add(new_farmer)

    db.commit()

    db.refresh(new_farmer)

    return new_farmer

@router.get("/{farmer_id}",response_model=FarmerResponse)
def get_farmer_byID(farmer_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Farmer).filter(Farmer.id==farmer_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id not found"
        )
    return item

@router.put("/{farmer_id}", response_model=FarmerResponse)
def update_farmer(farmer_id: UUID, farmer: FarmerUpdate, db:Session = Depends(get_db)):
    item = db.query(Farmer).filter_by(id=farmer_id).first()

    if item is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {farmer_id} not found"
        )

    if farmer.name is not None:
        item.name = farmer.name

    if farmer.phone is not None:
        item.phone = farmer.phone

    if farmer.preferred_lang is not None:
        item.preferred_lang = farmer.preferred_lang

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{farmer_id}")
def delete_farmer(farmer_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Farmer).filter_by(id=farmer_id).first()

    if item:
        db.delete(item)
        db.commit()
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {farmer_id} not found"
        )

    return {"message": f"Farmer deleted successfully"}
