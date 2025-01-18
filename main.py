import googlemaps
from datetime import datetime
import app
import time

jsonsave = app.json_update()

while True:
    now = datetime.now()
    time.sleep(1)
    if jsonsave != app.json_update():
        gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')

        # Récupération des données nécessaires
        geolocation_result = gmaps.geolocate()
        lat = geolocation_result['location']['lat']
        lng = geolocation_result['location']['lng']

        depart = app.json_catch("depart")
        arrivee = app.json_catch("arrivee")
        mode = app.json_catch("mode")
        mode = "w"  # Test : mode par défaut

        if mode == "t":
            coefficient = float(app.json_catch("WCoef"))
            choix = "transit"
        elif mode == "c":
            coefficient = float(app.json_catch("CCoef"))
            choix = "driving"
        else:
            coefficient = float(app.json_catch("WCoef"))
            choix = "walking"

        # Obtenir les directions
        output = gmaps.directions(depart, arrivee, mode=choix, departure_time=now)

        # Fonctions utilitaires
        def sec_to_min(ina):
            if ina < 3600:
                return f"{int(ina // 60)} min"
            else:
                no_h = (ina // 60) // 60
                no_m = (ina // 60) % 60
                return f"{int(no_h)} h {int(no_m)} min"

        def coef_update(inp):
            global coefficient  # Utilisation correcte de la portée locale
            if mode == "t":
                if inp == "y":
                    coefficient -= 0.02
                elif inp == "n":
                    coefficient += 0.02
                app.json_edit("WCoef", coefficient)

            elif mode == "c":
                if inp == "y":
                    coefficient -= 0.05
                elif inp == "n":
                    coefficient += 0.05
                app.json_edit("CCoef", coefficient)

            else:  # Par défaut, "walking"
                if inp == "y":
                    coefficient -= 0.05
                elif inp == "n":
                    coefficient += 0.05
                app.json_edit("WCoef", coefficient)

        # Traitement des résultats
        if output:
            route = output[0]
            leg = route['legs'][0]

            if mode == "t":  # Mode transit
                total_seconds = 0
                for elt in leg['steps']:
                    if elt["travel_mode"] == "WALKING":
                        total_seconds += elt["duration"]["value"] * coefficient
                    else:
                        total_seconds += elt["duration"]["value"]
                corrected_time = sec_to_min(total_seconds)
                print(f"Corrected Transit Time: {corrected_time}")

            else:  # Modes walking et driving
                estimated = leg['duration']['value']
                corrected_time = int(estimated * coefficient)
                corrected_time = sec_to_min(corrected_time)
                print(f"Estimated Time: {corrected_time}")
        else:
            print("No directions found!")
            corrected_time = "N/A"

        # Mise à jour du fichier JSON
        app.json_edit("estimated time", corrected_time)
        app.json_edit("faster", "o")  # Prépare le champ pour l'utilisateur

        # Attente de la réponse de l'utilisateur
        while app.json_catch("faster") == "o":
            time.sleep(1)
            if jsonsave != app.json_update():
                if app.json_catch("faster") == "y":
                    coef_update("y")
                elif app.json_catch("faster") == "n":
                    coef_update("n")
                else:
                    app.json_edit("faster", "o")

        # Actualiser la sauvegarde JSON
        jsonsave = app.json_update()
