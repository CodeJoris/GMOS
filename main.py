from flask import Flask, request, render_template_string
import googlemaps
from datetime import datetime
import jsonmaster  # Changed import from 'app' to 'jsonmaster'

app = Flask(__name__)

# HTML template for the input form
with open("index.html", "r", encoding="utf-8") as file:
    html_template = file.read()

# Default placeholder map
PLACEHOLDER_MAP_URL = "https://maps.googleapis.com/maps/api/staticmap?center=Montreal,QC&zoom=12&size=600x400&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

@app.route('/')
def home():
    return render_template_string(html_template, result=None, map_url=PLACEHOLDER_MAP_URL, depart=None, arrivee=None)

@app.route('/directions', methods=['POST'])
def get_directions():
    gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')
    now = datetime.now()

    # Get form data
    depart = request.form.get('depart')
    arrivee = request.form.get('arrivee')
    mode = request.form.get('mode', 'walking').lower()

    # Update JSON
    jsonmaster.json_edit("depart", depart)
    jsonmaster.json_edit("arrivee", arrivee)
    jsonmaster.json_edit("mode", mode)

    if mode == "transit":
        coefficient = float(jsonmaster.json_catch("WCoef", 1.0))
        choix = "transit"
    elif mode == "driving":
        coefficient = float(jsonmaster.json_catch("CCoef", 1.0))
        choix = "driving"
    else:
        coefficient = float(jsonmaster.json_catch("WCoef", 1.0))
        choix = "walking"

    try:
        # Get directions from Google Maps API
        directions = gmaps.directions(depart, arrivee, mode=choix, departure_time=now)
        leg = directions[0]['legs'][0]
        steps = leg['steps']
        path = "|".join([f"{step['end_location']['lat']},{step['end_location']['lng']}" for step in steps])

        # Corrected start and end addresses from Google Maps API
        corrected_depart = leg['start_address']
        corrected_arrivee = leg['end_address']

        # Build the static map URL with the path
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&markers=color:red|{corrected_depart}&markers=color:green|{corrected_arrivee}&path=color:0x0000ff|weight:5|{path}&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

        if directions:
            total_seconds = leg["duration"]["value"] * coefficient
            corrected_time = sec_to_min(total_seconds)
            jsonmaster.json_edit("estimated time", corrected_time)
            jsonmaster.json_edit("initial_time", total_seconds)
        else:
            corrected_time = "No directions found!"
            jsonmaster.json_edit("estimated time", corrected_time)
            jsonmaster.json_edit("initial_time", 0)
    except Exception as e:
        corrected_time = f"Error: {str(e)}"
        corrected_depart = "Unknown"
        corrected_arrivee = "Unknown"
        jsonmaster.json_edit("estimated time", corrected_time)
        jsonmaster.json_edit("initial_time", 0)

    # Render the template with the corrected addresses
    return render_template_string(html_template, result=corrected_time, map_url=map_url, depart=corrected_depart, arrivee=corrected_arrivee)

@app.route('/update_coefficient', methods=['POST'])
def update_coefficient():
    status = request.form.get('status')
    mode = jsonmaster.json_catch("mode", "walking") 
    coefficient = float(jsonmaster.json_catch("WCoef", 1.0))  
    initial_time = jsonmaster.json_catch("initial_time", 0)

    if status == "faster":
        coefficient -= 0.05
    elif status == "slower":
        coefficient += 0.05 
    elif status == "ontime":
        pass  

    if mode == "driving":
        jsonmaster.json_edit("CCoef", coefficient) 
    else:
        jsonmaster.json_edit("WCoef", coefficient)  

    # Reset to placeholder map
    return render_template_string(html_template, 
                                  result=None, 
                                  map_url=PLACEHOLDER_MAP_URL, 
                                  depart=None, 
                                  arrivee=None)

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
