from flask import Flask, request, render_template_string
import googlemaps
from datetime import datetime
import jsonmaster  # Changed import from 'app' to 'jsonmaster'

app = Flask(__name__)

# HTML template for the input form
with open("index.html", "r", encoding="utf-8") as file:
    html_template = file.read()

@app.route('/')
def home():
    # Set the placeholder map URL for Montreal as the initial map
    map_url = "https://maps.googleapis.com/maps/api/staticmap?center=Montreal,QC&zoom=12&size=600x400&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"
    return render_template_string(html_template, result=None, map_url=map_url)

@app.route('/directions', methods=['POST'])
def get_directions():
    gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')
    now = datetime.now()
    map_url = "https://maps.googleapis.com/maps/api/staticmap?center=Montreal,QC&zoom=12&size=600x400&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"  # Placeholder map

    # Get form data and update JSON
    depart = request.form.get('depart')
    arrivee = request.form.get('arrivee')
    mode = request.form.get('mode', 'walking').lower()

    jsonmaster.json_edit("depart", depart)
    jsonmaster.json_edit("arrivee", arrivee)
    jsonmaster.json_edit("mode", mode)

    if mode == "transit":
        coefficient = float(jsonmaster.json_catch("WCoef", 1.0))  
        choix = "transit"
    elif mode == "driving":
        coefficient = float(jsonmaster.json_catch("CCoef", 1.0))  
        choix = "driving"
    else:  # Default to walking
        coefficient = float(jsonmaster.json_catch("WCoef", 1.0))  
        choix = "walking"

    try:
        # Get directions from Google Maps API
        directions = gmaps.directions(depart, arrivee, mode=choix, departure_time=now)
        steps = directions[0]['legs'][0]['steps']
        path = "|".join([f"{step['end_location']['lat']},{step['end_location']['lng']}" for step in steps])

        # Build the static map URL with the path
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&markers=color:red|{depart}&markers=color:green|{arrivee}&path=color:0x0000ff|weight:5|{path}&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

        if directions:
            route = directions[0]
            leg = route['legs'][0]

            if choix == "transit":
                total_seconds = sum(
                    step["duration"]["value"] * coefficient if step["travel_mode"] == "WALKING" else step["duration"]["value"]
                    for step in leg["steps"]
                )
            else:
                estimated = leg["duration"]["value"]
                total_seconds = estimated * coefficient

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

    # Render the template with the result and map_url
    return render_template_string(html_template, result=corrected_time, map_url=map_url)

@app.route('/update_coefficient', methods=['POST'])
def update_coefficient():
    status = request.form.get('status')
    mode = jsonmaster.json_catch("mode", "walking") 
    coefficient = float(jsonmaster.json_catch("WCoef", 1.0))  
    initial_time = jsonmaster.json_catch("initial_time", 0)

    # Adjust the coefficient based on user input
    if status == "faster":
        coefficient -= 0.05
    elif status == "slower":
        coefficient += 0.05 
    elif status == "ontime":
        pass  
    
    # Update coefficient in the JSON file based on mode
    if mode == "driving":
        jsonmaster.json_edit("CCoef", coefficient) 
    else:
        jsonmaster.json_edit("WCoef", coefficient)  

    # Provide feedback to user and render the result
    jsonmaster.json_edit("estimated time", f"Coefficient updated to: {coefficient}")

    # Set the placeholder or real map URL
    map_url = "https://maps.googleapis.com/maps/api/staticmap?center=Montreal,QC&zoom=12&size=600x400&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

    # If the directions were already computed, reuse the map_url with the route
    if jsonmaster.json_catch("depart") and jsonmaster.json_catch("arrivee"):
        depart = jsonmaster.json_catch("depart")
        arrivee = jsonmaster.json_catch("arrivee")
        steps = jsonmaster.json_catch("steps", [])
        if steps:
            path = "|".join([f"{step['end_location']['lat']},{step['end_location']['lng']}" for step in steps])
            map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&markers=color:red|{depart}&markers=color:green|{arrivee}&path=color:0x0000ff|weight:5|{path}&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

    return render_template_string(html_template, result=f"Coefficient updated to: {coefficient}", map_url=map_url)

def sec_to_min(seconds):
    """Convert seconds to hours and minutes."""
    if seconds < 3600:
        return f"{int(seconds // 60)} min"
    else:
        no_h = (seconds // 60) // 60
        no_m = (seconds // 60) % 60
        return f"{int(no_h)} h {int(no_m)} min"

if __name__ == '__main__':
    app.run(debug=True)
