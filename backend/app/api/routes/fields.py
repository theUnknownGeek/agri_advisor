from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import Field
from typing import List
from app.schemas import FieldUpdate, FieldCreate,FieldResponse
from uuid import UUID
from decimal import Decimal

router = APIRouter(
    prefix="/fields",
    tags=["/fields"]
)

@router.get("/", response_model=List[FieldResponse])
def get_field(db: Session = Depends(get_db)):
    fields = db.query(Field).all()
    return fields

@router.post("/", response_model=FieldResponse)
def add_fields(
    field: FieldCreate,
    db: Session = Depends(get_db)
):  
    new_field = Field(
        farm_id = field.farm_id,
        name = field.name,
        area = field.area,
        area_unit = field.area_unit,
        soil_type = field.soil_type
    )

    db.add(new_field)
    db.commit()
    db.refresh(new_field)

    return new_field

@router.get("/{field_id}", response_model=FieldResponse)
def get_field_byID(field_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Field).filter(Field.id == field_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Field not found"
        )

    return item

@router.put("/{field_id}", response_model=FieldResponse)
def update_field(field_id: UUID, field: FieldUpdate, db:Session = Depends(get_db)):
    item = db.query(Field).filter(Field.id == field_id).first()

    if item is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id not found"
        )

    if field.name is not None:
            item.name = field.name

    if field.area is not None:
        item.area = field.area

    if field.area_unit is not None:
        item.area_unit = field.area_unit

    if field.soil_type is not None:
        item.soil_type = field.soil_type

    db.commit()
    db.refresh(item)

    return item

@router.delete("/{field_id}")
def del_field(field_id: UUID, db:Session = Depends(get_db)):
    item = db.query(Field).filter(Field.id == field_id).first()

    if item:
        db.delete(item)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id not found"
        )

    return {"message": f"Field with the given id deleted successfully"}