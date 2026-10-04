console.log("register.js is loaded");

const soilWeatherSection = document.getElementById("soil-weather-section");
const generateRecommendationButton = document.getElementById(
  "generate-recommendation",
);

let farmerId = null;

const farmerSection = document.getElementById("farmer-section");
const farmSection = document.getElementById("farm-section");
const fieldSection = document.getElementById("field-section");
const cropSection = document.getElementById("crop-section");
const farmerNext = document.getElementById("farmer-next");
const farmNext = document.getElementById("farm-next");
const fieldNext = document.getElementById("field-next");
const cropNext = document.getElementById("create-crop");

farmerNext.addEventListener("click", async function () {
  console.log("Farmer Next Clicked");

  try {
    farmerNext.innerText = "Creating...";
    farmerNext.disabled = true;

    const farmerData = {
      name: document.getElementById("farmer-name").value,

      phone: document.getElementById("farmer-Phone").value,

      preferred_lang: document.getElementById("farmer-language").value,
    };

    console.log("Sending Farmer Data: ", farmerData);

    const farmer = await createFarmer(farmerData);

    console.log("Farmer Created:", farmer);

    farmerId = farmer.id;

    console.log("farmer id is saved", farmerId);

    farmerSection.style.display = "none";

    farmSection.style.display = "block";
  } catch (error) {
    console.log(error);

    alert(error.message);
  } finally {
    farmerNext.innerText = "Next";
    farmerNext.disabled = false;
  }
});

let farmId = null;

farmNext.addEventListener("click", async function () {
  console.log("Farm Next Clicked");

  try {
    farmNext.innerText = "Creating...";
    farmNext.disabled = true;

    const farmData = {
      farmer_id: farmerId,
      name: document.getElementById("farm-name").value,
      latitude: document.getElementById("farm-latitude").value,
      longitude: document.getElementById("farm-longitude").value,
      area: document.getElementById("farm-area").value,
      area_unit: document.getElementById("farm-area-unit").value,
    };

    console.log("Sending farm data", farmData);

    const farm = await createFarm(farmData);

    console.log("farm created", farm);

    farmId = farm.id;

    console.log("Farm id is saved", farmId);

    farmSection.style.display = "none";

    fieldSection.style.display = "block";
  } catch (error) {
    console.log(error);
    alert(error.message);
  } finally {
    farmNext.innerText = "Next";
    farmNext.disabled = false;
  }
});

let fieldId = null;

fieldNext.addEventListener("click", async function () {
  console.log("Field Next Clicked");

  try {
    fieldNext.innerText = "Creating...";
    fieldNext.disabled = true;

    const fieldData = {
      farm_id: farmId,
      name: document.getElementById("field-name").value,
      area: document.getElementById("field-area").value,
      area_unit: document.getElementById("field-area-unit").value,
      soil_type: document.getElementById("field-soil").value,
    };

    console.log("Sending field data", fieldData);

    const field = await createField(fieldData);

    console.log("field created", field);

    fieldId = field.id;

    console.log("Field id is saved", fieldId);

    fieldSection.style.display = "none";
    cropSection.style.display = "block";
  } catch (error) {
    console.log(error);
    alert(error.message);
  } finally {
    fieldNext.innerText = "Next";
    fieldNext.disabled = false;
  }
});

let cropId = null;

cropNext.addEventListener("click", async function () {
  console.log("Crop Next Clicked");

  try {
    cropNext.innerText = "Creating...";
    cropNext.disabled = true;

    const cropData = {
      field_id: fieldId,
      crop: document.getElementById("crop").value,
      variety: document.getElementById("variety").value,
      season: document.getElementById("season").value,
      planting_date: document.getElementById("planting-date").value,
      establishment_method: document.getElementById("establishment-method")
        .value,
      current_growth_stage: document.getElementById("growth-stage").value,
    };

    console.log("Sending Crop data", cropData);

    const crop = await createCropCycle(cropData);

    console.log("crop created", crop);

    cropId = crop.id;

    console.log("Crop id is saved", cropId);

    cropSection.style.display = "none";
    soilWeatherSection.style.display = "block";
  } catch (error) {
    console.log(error);
    alert(error.message);
  } finally {
    cropNext.innerText = "Create Farmer Profile";
    cropNext.disabled = false;
  }
});

generateRecommendationButton.addEventListener("click", async function () {
  console.log("Generate Recommendation Clicked");

  try {
    generateRecommendationButton.innerText = "Generating...";
    generateRecommendationButton.disabled = true;

    // =========================
    // SOIL DATA
    // =========================

    const soilData = {
      field_id: fieldId,

      moisture_percentage: document.getElementById("soil-moisture").value,

      recorded_at: document.getElementById("soil-recorded-at").value,

      source_soil: document.getElementById("soil-source").value,
    };

    console.log("Sending Soil Data:", soilData);

    const soil = await createSoilMoisture(soilData);

    console.log("Soil data created");

    // =========================
    // WEATHER DATA
    // =========================

    const weatherData = {
      field_id: fieldId,

      timestamp: document.getElementById("weather-timestamp").value,

      temperature: document.getElementById("weather-temperature").value,

      humidity: document.getElementById("weather-humidity").value,

      rainfall: document.getElementById("weather-rainfall").value,

      rain_probability: document.getElementById("weather-rain-probability")
        .value,

      wind_speed: document.getElementById("weather-wind-speed").value || null,

      data_type: document.getElementById("weather-data-type").value,
    };

    console.log("Sending Weather Data:", weatherData);

    const rain = await createWeatherData(weatherData);

    console.log("Weather data created");

    // =========================
    // GENERATE RECOMMENDATION
    // =========================

    console.log("Generating recommendation...");

    const recommendation = await generateRecommendation(cropId);

    console.log("Recommendation generated:", recommendation);

    // =========================
    // OPEN DASHBOARD
    // =========================

    window.location.href = `dashboard.html?id=${cropId}`;
  } catch (error) {
    console.log(error);

    alert(error.message);
  } finally {
    generateRecommendationButton.innerText = "Generate Recommendation";

    generateRecommendationButton.disabled = false;
  }
});
