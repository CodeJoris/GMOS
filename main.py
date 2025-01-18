import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')
now = datetime.now()
depart = input("Where are you ?")
arrivee = input("Where do you want to go ?")
output = gmaps.directions(depart,arrivee,mode="walking",departure_time=now)

if output:
    route = output[0]
    leg = route['legs'][0]
    estimated=leg['duration']['text']
    print(f"Estimated Time: ", estimated)
else:
    print("No directions found!")
