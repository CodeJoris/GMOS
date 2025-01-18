    
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

        mode = input("How do you want to get there: walking (W), transit (T), car (C)? ").lower()
        choix = "walking"
        if mode == "t" or mode == "transit":
            choix = "transit"
            with open("WCoef.txt", "r") as file:
                coefficient = float(file.readline().strip())
        elif mode == "c" or mode == "car":
            choix = "driving"
            with open("CCoef.txt", "r") as file:
                coefficient = float(file.readline().strip())
        else:
            with open("WCoef.txt", "r") as file:
                coefficient = float(file.readline().strip())

        output = gmaps.directions((lat,lng), arrivee, mode=choix, departure_time=now)

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
                filename = "WCoef.txt"
            elif choix == "driving":
                filename = "CCoef.txt"
            else:
                filename = "WCoef.txt"

            with open(filename, "w") as file:
                if inp in ("y", "yes"):
                    coefficient -= 0.05
                elif inp in ("n", "no"):
                    coefficient += 0.05
                file.write(str(coefficient))  # Update the file with the new coefficient

        if output:
            route = output[0]
            leg = route['legs'][0]
            ##print(leg)
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

        answer = input("Did you reach your destination faster or slower than expected? (Y/N): ").lower()
        coef_update(answer)

        # Save to a text file
        with open("data.txt", "w") as file:
            file.write(str(coefficient))
        jsonsave=app.json_update()
