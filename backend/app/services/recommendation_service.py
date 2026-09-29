from app.ai.rule_engine import generate_recommendation
from app.models import Recommendation

def create_recommendation(db, soil_moisture, rain_probability, crop_cycle_id):
    result = generate_recommendation(soil_moisture,rain_probability)

    new_recommendation =  Recommendation(
        crop_cycle_id = crop_cycle_id,
        decision = result["decision"],
        reason = result["reason"],
        confidence = result["confidence"],
        status = result["status"]
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return new_recommendation