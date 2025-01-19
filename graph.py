import jsonmaster
import googlemaps
from datetime import datetime
import json



def correction(mot):
    dico=  {'Rue University': 'University',
    'Rue Prince Arthur O': 'Prince',
    'Rue Durocher': 'Durocher',
    'Av des Pins O': 'Pins',
    'Av. du Parc': 'Parc',
    'Chem. de la Côte-Sainte-Catherine': 'Côte-Sainte-Catherine',
    'Av. Victoria': 'Victoria',
    'Bd Édouard-Montpetit': 'Edouard-Montpetit',
    'Rue Lemieux': 'Lemieux'}
    if mot in dico:
        return dico[mot]

directions=jsonmaster.json_read("directions.json")

legs = directions["legs"][0]
locs = []
for step in legs["steps"]:
    try:
        locs.append(correction(step["html_instructions"].split("<b>")[2].split("</b>")[0]))
    except:
        continue

with open('feux.json', 'r') as fichier:
    data = json.load(fichier)

graph = {}
for feature in data['features']:
    rue1 = feature['properties']['RUE_1']
    rue2 = feature['properties']['RUE_2']

    if rue1 not in graph:
        graph[rue1] = []
    if rue2 not in graph:
        graph[rue2] = []

    if rue2 not in graph[rue1]:
        graph[rue1].append(rue2)
    if rue1 not in graph[rue2]:
        graph[rue2].append(rue1)



print(locs)
nb_feux = 0
for i in range(len(locs)-1):
    rue1 = locs[i]
    rue2 = locs[i+1]
    if rue1 in graph:
        if rue2 in graph[rue1]:
            nb_feux += 1
    if rue2 in graph:
        if rue1 in graph[rue2]:
            nb_feux += 1



print(nb_feux)