def irrigation_rules(soil_moisture,rain_probability):
    if soil_moisture<30 and rain_probability>40:
        return{
            "decision": "IRRIGATE",
            "reason": "Low soil moisture and low chances of rainfall",
            "confidence": "0.90",
            "status": "ACTIVE"
        }

    elif soil_moisture>=30 and rain_probability>60:
        return{
            "decision": "WAIT",
            "reason": "Sufficient moisture and rainfall expected",
            "confidence": "0.85",
            "status": "ACTIVE"
        }

    else:
        return{
            "decision": "MONITOR",
            "reason": "Conditions are normal, continue monitoring",
            "confidence": 0.70,
            "status": "ACTIVE"
        }