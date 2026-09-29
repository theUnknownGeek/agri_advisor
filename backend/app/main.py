from fastapi import FastAPI, Depends
from app.api.routes import farmers, farms, fields,crop_cycles, irrigation_records, recommendation, soil_moisture, weather_data, dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farmers.router)
app.include_router(farms.router)
app.include_router(fields.router)
app.include_router(crop_cycles.router)
app.include_router(irrigation_records.router)
app.include_router(recommendation.router)
app.include_router(soil_moisture.router)
app.include_router(weather_data.router)
app.include_router(dashboard.router)

@app.get("/")
def send_greet():
    return {"message": "Hello this checkpoint is working fine"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}