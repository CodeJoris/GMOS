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

if output:  # Check if the output is not empty
    # Extract the first route and leg
    route = output[0]
    leg = route['legs'][0]

    # Print overall route information
    print("Route Overview:")
    print(f"From: {leg['start_address']}")
    print(f"To: {leg['end_address']}")
    print(f"Total Distance: {leg['distance']['text']}")
    print(f"Estimated Time: {leg['duration']['text']}")
    print()

    # Print step-by-step directions
    print("Step-by-Step Directions:")
    for step in leg['steps']:
        instruction = step['html_instructions']
        distance = step['distance']['text']
        duration = step['duration']['text']
        # Remove HTML tags from instructions for clean printing
        import re
        clean_instruction = re.sub(r'<.*?>', '', instruction)
        print(f"- {clean_instruction} ({distance}, {duration})")
else:
    print("No directions found!")
