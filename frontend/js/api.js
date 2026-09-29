const API_URL = "http://localhost:8000";



async function getDashboardData(cropCycleId){


    const response = await fetch(
        `${API_URL}/dashboard/${cropCycleId}`
    );


    if(!response.ok){

        throw new Error(
            "Failed to fetch dashboard data"
        );

    }


    return await response.json();


}