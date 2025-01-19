import jsonmaster
import googlemaps
from datetime import datetime
import json


directions=jsonmaster.json_read("directions.json")

legs = directions["legs"][0]
for step in legs["steps"]:
    print(step["html_instructions"])
    print(step["distance"]["text"])
    print(step["duration"]["text"])
    print("")