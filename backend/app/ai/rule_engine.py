from app.ai.irrigation_rules import irrigation_rules

def generate_recommendation(soil_moisture, rain_probability):
    result = irrigation_rules(soil_moisture, rain_probability)
    return result
