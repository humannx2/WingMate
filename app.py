import pandas as pd
import os
from dotenv import load_dotenv
from opensky_api import OpenSkyApi
# print("OpenSky API installed correctly!")

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

api = OpenSkyApi(USERNAME, PASSWORD)
states = api.get_states()
if states is not None:
    print(states)
else:
    print("No states found")

# states = api.get_states(bbox=(45.8389, 47.8229, 5.9962, 10.5226))
# for s in states.states:
#     print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))


