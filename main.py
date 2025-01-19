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
    start_address = "123 Main St, Cityville"  # Replace with the actual start address
    end_address = "456 Elm St, Townsville"   # Replace with the actual end address
    return render_template_string(html_template, result=None, map_url=None)

@app.route('/directions', methods=['POST'])

def get_directions():
    gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')
    now = datetime.now()

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
            start_address = leg['start_address']
            end_address = leg['end_address']

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

@app.route('/start_address', methods=['POST'])
def start_address():
    start_address = request.form.get('start_address')
    return render_template_string(html_template, start_address=start_address, end_address=None)

@app.route('/end_address', methods=['POST'])
def end_address():
    end_address = request.form.get('end_address')
    return render_template_string(html_template, start_address=None, end_address=end_address)

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

    # Provide feedback to user and render the result
    jsonmaster.json_edit("estimated time", f"Coefficient updated to: {coefficient}")
    return render_template_string(html_template, result=f"Coefficient updated to: {coefficient}")

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
