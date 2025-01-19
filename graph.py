import jsonmaster
import googlemaps
from datetime import datetime
import json

def get_directions():
    gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')  # Replace with your API key
    now = datetime.now()
    
    depart = 'Trottier Space Institute McGil'
    arrivee = '4917 rue Fulton'
    choix = 'walking'

    try:
        # Get directions from Google Maps API
        directions = gmaps.directions(depart, arrivee, mode=choix, departure_time=now)
        with open('directions.json', 'w') as f:
            json.dump(directions, f)

        if directions:
            route = directions[0]
            leg = route['legs'][0]

            if choix == "transit":
                total_seconds = sum(
                    step["duration"]["value"] if step["travel_mode"] == "WALKING" else step["duration"]["value"]
                    for step in leg["steps"]
                )
            else:
                estimated = leg["duration"]["value"]
                total_seconds = estimated 

            corrected_time = sec_to_min(total_seconds)
            jsonmaster.json_edit("estimated time", corrected_time)
            jsonmaster.json_edit("initial_time", total_seconds)
        else:
            corrected_time = "No directions found!"
            jsonmaster.json_edit("estimated time", corrected_time)
            jsonmaster.json_edit("initial_time", 0)
    except Exception as e:
        corrected_time = f"Error: {str(e)}"
        jsonmaster.json_edit("estimated time", corrected_time)
        jsonmaster.json_edit("initial_time", 0)

    def sec_to_min(seconds):
        """Convert seconds to hours and minutes."""
        if seconds < 3600:
            return f"{int(seconds // 60)} min"
        else:
            no_h = (seconds // 60) // 60
            no_m = (seconds // 60) % 60
            return f"{int(no_h)} h {int(no_m)} min"
        
get_directions()
