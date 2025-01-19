from flask import Flask, request, render_template_string
import googlemaps
from datetime import datetime
import jsonmaster, lights  # Changed import from 'app' to 'jsonmaster'


app = Flask(__name__)
jsonmaster.json_edit("WCoef", 1.0)
jsonmaster.json_edit("CCoef", 1.0)
jsonmaster.json_edit("number of changes", 0)

# HTML template for the input form
with open("index.html", "r", encoding="utf-8") as file:
    html_template = file.read()

# Default placeholder map
PLACEHOLDER_MAP_URL = "https://maps.googleapis.com/maps/api/staticmap?center=Montreal,QC&zoom=12&size=600x400&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"

@app.route('/')
def home():
    w_coef = jsonmaster.json_catch("WCoef",1.0)
    c_coef = jsonmaster.json_catch("CCoef",1.0)
    return render_template_string(html_template, result=None, map_url=PLACEHOLDER_MAP_URL, depart=None, arrivee=None,w_coef=w_coef,c_coef=c_coef)

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

        virgule1= prendre_avant_virgule(corrected_depart)
        virgule2= prendre_avant_virgule(corrected_arrivee)

        # Build the static map URL with the path
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&markers=color:red|{corrected_depart}&markers=color:green|{corrected_arrivee}&path=color:0x0000ff|weight:5|{path}&key=AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ"
       
        if directions:
            total_seconds = leg["duration"]["value"] * coefficient
            corrected_time = sec_to_min(total_seconds)

            # count the estimated traffic lights
            counted = False
            if total_seconds < 4000:
                crossing_spots = lights.count_crossing_spots(depart, arrivee)
                
                temp = crossing_spots * 10
                time_interval = (sec_to_min(total_seconds - temp), sec_to_min(total_seconds + temp))
                
                jsonmaster.json_edit("min time", time_interval[0])
                jsonmaster.json_edit("max time", time_interval[1])
                jsonmaster.json_edit("crossing", crossing_spots)

                counted = True
            
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

    w_coef = jsonmaster.json_catch("WCoef",1.0)
    c_coef = jsonmaster.json_catch("CCoef",1.0)
    if counted:
        min_time = jsonmaster.json_catch("min time", 1.0)
        max_time = jsonmaster.json_catch("max time", 1.0)
        # Render the template with the corrected addresses
        return render_template_string(html_template, result=corrected_time, map_url=map_url, depart=corrected_depart, arrivee=corrected_arrivee, w_coef=w_coef, c_coef=c_coef, min_time=min_time, max_time=max_time)
    return render_template_string(html_template, result=corrected_time, map_url=map_url, depart=corrected_depart, arrivee=corrected_arrivee, w_coef=w_coef, c_coef=c_coef, min_time='too long', max_time='too long',virgule1=virgule1,virgule2=virgule2)

@app.route('/update_coefficient', methods=['POST'])
def update_coefficient():
    status = request.form.get('status')
    mode = jsonmaster.json_catch("mode", "walking") 
    coefficient = float(jsonmaster.json_catch("WCoef", 1.0))  
    initial_time = jsonmaster.json_catch("initial_time", 0)

    num_changes = jsonmaster.json_catch("number of changes", 1.0)
    scale_factor = max(0.01, 1 / (num_changes + 1))  # Ensure scale_factor doesn't go below 0.01

    if status == "faster":
        coefficient -= 0.05 * scale_factor
        coefficient = round(coefficient, 5)
        iterate_change()
    elif status == "slower":
        coefficient += 0.05 * scale_factor
        coefficient = round(coefficient, 5)
        iterate_change()
    elif status == "ontime":
        iterate_change()
        pass

    if mode == "driving":
        jsonmaster.json_edit("CCoef", coefficient) 
    else:
        jsonmaster.json_edit("WCoef", coefficient)  

    # Reset to placeholder map
    w_coef = jsonmaster.json_catch("WCoef",1.0)
    c_coef = jsonmaster.json_catch("CCoef",1.0)
    # Render the template with the corrected addresses
    #return render_template_string(html_template, result=corrected_time, map_url=map_url, depart=corrected_depart, arrivee=corrected_arrivee, w_coef=w_coef, c_coef=c_coef)
    return render_template_string(html_template, 
                                  result=None, 
                                  map_url=PLACEHOLDER_MAP_URL, 
                                  depart=None, 
                                  arrivee=None,w_coef=w_coef, c_coef=c_coef)

def sec_to_min(seconds):
    """Convert seconds to hours and minutes."""
    if seconds < 3600:
        return f"{int(seconds // 60)} min"
    else:
        no_h = (seconds // 60) // 60
        no_m = (seconds // 60) % 60
        return f"{int(no_h)} h {int(no_m)} min"

def iterate_change():
    nb = jsonmaster.json_catch("number of changes", 1.0)
    jsonmaster.json_edit("number of changes", nb+1)

def prendre_avant_virgule(mot):
    return mot.split(",")[0]
if __name__ == '__main__':
    app.run(debug=True)
