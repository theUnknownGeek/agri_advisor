from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import IrrigationLog
from typing import List
from app.schemas import IrrigationLogUpdate, IrrigationLogCreate, IrrigationLogResponse
from uuid import UUID
from decimal import Decimal


router = APIRouter(
    prefix="/irrigation_logs",
    tags=["/irrigation_logs"]
)


@router.get("/", response_model=List[IrrigationLogResponse])
def get_irrigation_logs(db: Session = Depends(get_db)):
    irrigation_logs = db.query(IrrigationLog).all()
    return irrigation_logs


@router.post("/", response_model=IrrigationLogResponse)
def add_irrigation_log(
    irrigation_log: IrrigationLogCreate,
    db: Session = Depends(get_db)
):
    new_irrigation_log = IrrigationLog(
        field_id = irrigation_log.field_id,
        irrigation_date = irrigation_log.irrigation_date,
        duration_minutes = irrigation_log.duration_minutes,
        irrigation_amount = irrigation_log.irrigation_amount,
        amount_unit = irrigation_log.amount_unit
    )

    db.add(new_irrigation_log)
    db.commit()
    db.refresh(new_irrigation_log)

    return new_irrigation_log


@router.get("/{irrigation_log_id}", response_model=IrrigationLogResponse)
def get_irrigation_log_by_id(
    irrigation_log_id: UUID,
    db: Session = Depends(get_db)
):
    item = db.query(IrrigationLog).filter(
        IrrigationLog.id == irrigation_log_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Irrigation log not found"
        )

    return item


@router.put("/{irrigation_log_id}", response_model=IrrigationLogResponse)
def update_irrigation_log(
    irrigation_log_id: UUID,
    irrigation_log: IrrigationLogUpdate,
    db: Session = Depends(get_db)
):
    item = db.query(IrrigationLog).filter(
        IrrigationLog.id == irrigation_log_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Irrigation log not found"
        )


    if irrigation_log.irrigation_date is not None:
        item.irrigation_date = irrigation_log.irrigation_date

    if irrigation_log.duration_minutes is not None:
        item.duration_minutes = irrigation_log.duration_minutes

    if irrigation_log.irrigation_amount is not None:
        item.irrigation_amount = irrigation_log.irrigation_amount

    if irrigation_log.amount_unit is not None:
        item.amount_unit = irrigation_log.amount_unit


    db.commit()
    db.refresh(item)

    return item


@router.delete("/{irrigation_log_id}")
def delete_irrigation_log(
    irrigation_log_id: UUID,
    db: Session = Depends(get_db)
):
    item = db.query(IrrigationLog).filter(
        IrrigationLog.id == irrigation_log_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Irrigation log not found"
        )

    return {
        "message": "Irrigation log deleted successfully"
    }