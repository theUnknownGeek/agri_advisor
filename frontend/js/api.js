const API_URL = "http://localhost:8000";

async function apiRequest(url, option={}){
    const response = await fetch(url,option);

    if(!response.ok){
        const errorText = await response.text();

        console.error(
            "API ERROR: ",
            response.status,
            errorText
        );

        throw new Error(errorText || "API Request Failed");
    }

    return await response.json();
}

async function createFarmer(data){
    return await apiRequest(
        `${API_URL}/farmers/`,
    {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

async function createFarm(data){
    return await apiRequest(
        `${API_URL}/farms/`,
    {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

async function createField(data){
    return await apiRequest(
        `${API_URL}/fields/`,
    {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

async function createCropCycle(data){
    return await apiRequest(
        `${API_URL}/crop_cycles/`,
    {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    });
}
async function createSoilMoisture(data) {
    return await apiRequest(`${API_URL}/soil_moisture/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
}


async function createWeatherData(data) {
    return await apiRequest(`${API_URL}/weather_data/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

async function getDashboardData(cropCycleId){
    return await apiRequest(
        `${API_URL}/dashboard/${cropCycleId}/`
    )
}

async function generateRecommendation(cropCycleId) {
    return await apiRequest(
        `${API_URL}/recommendations/generate/${cropCycleId}`,
        {
            method: "POST"
        }
    );
}

window.createFarmer = createFarmer;
window.createFarm = createFarm;
window.createField = createField;
window.createCropCycle = createCropCycle;
window.getDashboardData = getDashboardData;
window.createSoilMoisture = createSoilMoisture;
window.createWeatherData = createWeatherData;
window.generateRecommendation = generateRecommendation;

console.log("api.js loaded successfully")