import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBw8lINwBQQ9t5tv02oBLwty-Kg6n3iLzQ')
now = datetime.now()
depart = input("Where are you ?")
arrivee = input("Where do you want to go ?")

mode = input("How do you want to get there : walking (W), transit (T), car (C) ?").lower()
choix="walking"
if mode == "t" or "transit":
    choix = "transit"
    with open("TCoef.txt", "r") as file:
        coefficient = float(file.readline())
elif mode == "c" or "car":
    choix = "car"
    with open("CCoef.txt", "r") as file:
        coefficient = float(file.readline())
else:
    with open("WCoef.txt", "r") as file:
        coefficient = float(file.readline())    


output = gmaps.directions(depart,arrivee,mode=choix,departure_time=now)

def sec_to_min(ina):
    if ina<3600:
        return (str(ina//60) + " min")
    else:
        no_h=(ina//60)//60
        no_m=(ina//60)%60
        return (str(no_h)+" h "+str(no_m)+ " min")
    
def coef_update(inp):

    with open("data.txt", "r") as file:
        if inp=="y" or inp=="yes":
            
            

if output:
    route = output[0]
    leg = route['legs'][0]
    estimated=leg['distance']['value'] #this is the estimated time by the API in seconds
    corrected_time = int((estimated)*coefficient)
    corrected_time = sec_to_min(corrected_time)
    print(f"Estimated Time: ", corrected_time)
else:
    print("No directions found!")



answer = input("Did you reach your destination faster or slower than expected ? (Y/N/SAME)").lower
if answer == "y" or "yes":
    if 
elif answer=="n" or "no":
    coefficient+=0.05


# Save to a text file
with open("data.txt", "w") as file:
    file.write(str(coefficient))
