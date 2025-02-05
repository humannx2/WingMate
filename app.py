import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("API_KEY")

BASE_URL = "http://api.aviationstack.com/v1/flights"

# params = {
#     "access_key": api_key,
#     # "dep_iata": "DEL",
#     "arr_iata": "BOM",
#     # "airline_iata": "6E",
#     "limit": 5  # Get the latest 5 flights
# }

def fetch_flight_data(params):
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        for flight in data['data']:
            print(f"Flight {flight['flight']['iata']} from {flight['departure']['airport']} to {flight['arrival']['airport']} is currently {flight['flight_status']}.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


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

# check_oldflight_status(params)






# fetch_flight_data(params)

