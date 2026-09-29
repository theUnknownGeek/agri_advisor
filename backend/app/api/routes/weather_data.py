from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models import WeatherData

from app.schemas import (
    WeatherDataCreate,
    WeatherDataUpdate,
    WeatherDataResponse
)



router = APIRouter(
    prefix="/weather_data",
    tags=["/weather_data"]
)



@router.get("/", response_model=List[WeatherDataResponse])
def get_weather_data(
    db: Session = Depends(get_db)
):

    data = db.query(WeatherData).all()

    return data




@router.post("/", response_model=WeatherDataResponse)
def add_weather_data(
    weather: WeatherDataCreate,
    db: Session = Depends(get_db)
):

    new_weather = WeatherData(

        field_id = weather.field_id,

        timestamp = weather.timestamp,

        temperature = weather.temperature,

        humidity = weather.humidity,

        rainfall = weather.rainfall,

        rain_probability = weather.rain_probability,

        wind_speed = weather.wind_speed,

        data_type = weather.data_type
    )


    db.add(new_weather)

    db.commit()

    db.refresh(new_weather)


    return new_weather





@router.get("/{weather_id}", response_model=WeatherDataResponse)
def get_weather_by_id(
    weather_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(WeatherData).filter(
        WeatherData.id == weather_id
    ).first()


    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found"
        )


    return item






@router.put("/{weather_id}", response_model=WeatherDataResponse)
def update_weather(
    weather_id: UUID,
    weather: WeatherDataUpdate,
    db: Session = Depends(get_db)
):

    item = db.query(WeatherData).filter(
        WeatherData.id == weather_id
    ).first()


    if item is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found"
        )



    if weather.timestamp is not None:
        item.timestamp = weather.timestamp


    if weather.temperature is not None:
        item.temperature = weather.temperature


    if weather.humidity is not None:
        item.humidity = weather.humidity


    if weather.rainfall is not None:
        item.rainfall = weather.rainfall


    if weather.rain_probability is not None:
        item.rain_probability = weather.rain_probability


    if weather.wind_speed is not None:
        item.wind_speed = weather.wind_speed


    if weather.data_type is not None:
        item.data_type = weather.data_type



    db.commit()

    db.refresh(item)


    return item






@router.delete("/{weather_id}")
def delete_weather(
    weather_id: UUID,
    db: Session = Depends(get_db)
):

    item = db.query(WeatherData).filter(
        WeatherData.id == weather_id
    ).first()


    if item:

        db.delete(item)

        db.commit()


    else:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found"
        )


    return {
        "message": "Weather data deleted successfully"
    }