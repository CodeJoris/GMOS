import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')

'''
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)

# Get an Address Descriptor of a location in the reverse geocoding response
address_descriptor_result = gmaps.reverse_geocode((40.714224, -73.961452), enable_address_descriptor=True)
'''
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