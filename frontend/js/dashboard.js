async function loadDashboard() {
  const params = new URLSearchParams(window.location.search);

  const id = params.get("id");

  if (!id) {
    alert("No Crop Cycle ID found");

    return;
  }

  try {
    const data = await getDashboardData(id);

    document.getElementById("crop").innerText = data.crop;

    document.getElementById("moisture").innerText = data.soil.moisture + "%";

    document.getElementById("temperature").innerText =
      data.weather.temperature + " °C";

    document.getElementById("humidity").innerText = data.weather.humidity + "%";

    document.getElementById("rain").innerText =
      data.weather.rain_probability + "%";

    document.getElementById("decision").innerText =
      data.recommendation.decision;

    document.getElementById("reason").innerText = data.recommendation.reason;

    document.getElementById("confidence").innerText =
      data.recommendation.confidence * 100 + "%";

    document.getElementById("status").innerText = data.recommendation.status;
  } catch (error) {
    console.log(error);

    alert("Unable to load dashboard");
  }
}

loadDashboard();
