import pandas as pd
import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI 
import uvicorn

load_dotenv()
api_key = os.getenv("API_KEY")

BASE_URL = "http://api.aviationstack.com/v1/flights"
app = FastAPI()

params = {
    "access_key": api_key,
    # "dep_iata": "DEL",
    "arr_iata": "BOM",
    "flight_status": "landed",
    # "airline_iata": "6E",
    "limit": 5  # Get the latest 5 flights
}

@app.get("/flights")  # Define a new endpoint
def fetch_flight_data_endpoint(arrival: str = None, departure: str = None, airline_num: str = None, flight_status: str = None, limit: int = 5):
    # Initialize an empty params dictionary
    params = {"access_key": api_key, "limit": limit}
    # Add parameters only if values are provided
    if departure:
        params["dep_iata"] = departure
    # if arrival:
    #     params["arr_iata"] = arrival
    if airline_num:
        params["airline_iata"] = airline_num
    if flight_status:
        params["flight_status"] = flight_status
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        flights_info = []
        for flight in data['data']:
            flights_info.append({
                "flight": flight['flight']['iata'],
                "departure": flight['departure']['airport'],
                "arrival": flight['arrival']['airport'],
                "status": flight['flight_status']
            })
        return {"flights": flights_info}  # Return flight data as JSON
    else:
        return {"error": f"Error: {response.status_code}, {response.text}"}  # Return error as JSON

# params = {
#     "access_key": api_key,
#     "flight_date": "2024-02-01",
#     "flight_status": "cancelled"
# }
# Current API plan doesn't support flight status
def check_oldflight_status(params):
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        for flight in data['data']:
            departure_scheduled = flight["departure"]["estimated"]
            departure_actual = flight["departure"]["actual"]
            arrival_scheduled = flight["arrival"]["estimated"]
            arrival_actual = flight["arrival"]["actual"]

            if departure_actual and departure_scheduled:
                delay_minutes = (
                    (pd.to_datetime(departure_actual) - pd.to_datetime(departure_scheduled)).seconds
                    if departure_actual > departure_scheduled else 0
                )

                print(f"Flight {flight['flight']['iata']} was delayed by {delay_minutes // 60} minutes.")
            else:
                print(f"Flight {flight['flight']['iata']} status: {flight['flight_status']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Gave internal server error
def get_airport_info(api_key, airport_iata):
    """
    Fetches airport information from the AviationStack API.

    Args:
        api_key (str): Your AviationStack API key.
        airport_iata (str): IATA code of the airport (e.g., "DEL" for Delhi).

    Returns:
        dict: Airport details or an error message.
    """
    base_url = "http://api.aviationstack.com/v1/airports"
    params = {
        "access_key": api_key,
        "iata_code": airport_iata  # Filter by IATA code
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]:
            airport = data["data"][0]  # Get the first matching airport
            return {
                "name": airport.get("airport_name"),
                "iata": airport.get("iata_code"),
                "icao": airport.get("icao_code"),
                "country": airport.get("country_name"),
                "city": airport.get("city"),
                "latitude": airport.get("latitude"),
                "longitude": airport.get("longitude"),
                "timezone": airport.get("timezone")
            }
        else:
            return {"error": "No airport data found for the given IATA code."}
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

# airport_code = "BLR"  # Example: Delhi Airport
# airport_info = get_airport_info(api_key, airport_code)

# if "error" in airport_info:
#     print(airport_info["error"])
# else:
#     print(f"Airport: {airport_info['name']} ({airport_info['iata']})")
#     print(f"Location: {airport_info['city']}, {airport_info['country']}")
#     print(f"Coordinates: {airport_info['latitude']}, {airport_info['longitude']}")
#     print(f"Timezone: {airport_info['timezone']}")





# check_oldflight_status(params)
# fetch_flight_data_endpoint()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

