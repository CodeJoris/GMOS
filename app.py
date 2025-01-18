import json


def json_edit(a,b):
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)  
    data[a] = b
    with open('infos.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)

def json_catch(a):
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)  
    return data[a] 

def json_update():
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)  
    return data















