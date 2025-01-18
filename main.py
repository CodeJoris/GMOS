    
import googlemaps
from datetime import datetime
import app
import time
jsonsave=app.json_update()
while True:
    now = datetime.now()
    time.sleep(1)
    if jsonsave!=app.json_update():
        gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')

        geolocation_result = gmaps.geolocate()
        lat = geolocation_result['location']['lat']
        lng = geolocation_result['location']['lng']

        depart = app.json_catch("depart")
        arrivee = app.json_catch("arrivee")

        mode = app.json_catch("mode")
        choix = "walking"
        if mode == "t" or mode == "transit":
            choix = "transit"
            coefficient = app.json_catch("WCoef")
        elif mode == "c" or mode == "car":
            choix = "driving"
            coefficient = app.json_catch("CCoef")
        else:
            coefficient = app.json_catch("WCoef")
    
        output = gmaps.directions(depart, arrivee, mode=choix, departure_time=now)

        def sec_to_min(ina):
            if ina < 3600:
                return f"{int(ina // 60)} min"
            else:
                no_h = (ina // 60) // 60
                no_m = (ina // 60) % 60
                return f"{int(no_h)} h {int(no_m)} min"

        def coef_update(inp):
            global coefficient
            if choix == "transit":
                if inp in ("y", "yes"):
                    app.json_edit("WCoef",str(float(app.json_catch("WCoef"))-0.02))
                elif inp in ("n", "no"):
                    app.json_edit("WCoef",str(float(app.json_catch("WCoef"))+0.02))
            elif choix == "driving":
                if inp in ("y", "yes"):
                    app.json_edit("WCoef",str(float(app.json_catch("CCoef"))-0.05))
                elif inp in ("n", "no"):
                    app.json_edit("WCoef",str(float(app.json_catch("WCoef"))+0.05))
            else:
                if inp in ("y", "yes"):
                    app.json_edit("WCoef",str(float(app.json_catch("WCoef"))-0.05))
                elif inp in ("n", "no"):
                    app.json_edit("WCoef",str(float(app.json_catch("WCoef"))+0.05))

        if output:
            route = output[0]
            leg = route['legs'][0]
            if choix=="transit":
                total_seconds=0
                for elt in leg['steps']:
                    if elt["travel_mode"]=="WALKING":
                        total_seconds+=elt["duration"]["value"]*coefficient
                        print(elt["duration"]["value"]*coefficient)
                    else:
                        total_seconds+=elt["duration"]["value"]
                        print(elt["duration"]["value"])
                corrected_time=sec_to_min(total_seconds)
                print(corrected_time)
            else:
                estimated = leg['duration']['value']  # Estimated time by the API in seconds
                corrected_time = int(estimated * coefficient)
                corrected_time = sec_to_min(corrected_time)
                print(f"Estimated Time: {corrected_time}")
        else:
            print("No directions found!")

        app.json_edit("estimated time",corrected_time)
        notupdated=True
        app.json_edit("faster","")
        while notupdated:
            if app.json_catch("faster")!="":
                answer = app.json_catch("faster")
                coef_update(answer)
                app.json_edit("faster","")
                notupdated=False

        jsonsave=app.json_update()
