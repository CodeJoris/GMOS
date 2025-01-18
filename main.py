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
    estimated=leg['duration']['text'] #this is the estimated time by the API
    print(f"Estimated Time: ", estimated)
else:
    print("No directions found!")

coefficient = 1

answer = input("Did you reach your destination faster or slower than expected ? (Y/N)").lower
if answer == "y" or "yes":
    coefficient-=0.05
elif answer=="n" or "no":
    coefficient+=0.05

# Save to a text file
with open("output.txt", "w") as file:
    file.write(coefficient)
