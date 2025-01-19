import json

def json_edit(a, b):
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)
    data[a] = b
    with open('infos.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)

def json_catch(a, default=None):

    try:
        with open('infos.json', 'r') as fichier:
            data = json.load(fichier)
        return data.get(a, default)
    except FileNotFoundError:
        return default 

def json_update():
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)
    return data

def json_read(a):
        with open(a, 'r') as fichier:
            return json.load(fichier)
