import json

def json_edit(a, b):
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)
    data[a] = b
    with open('infos.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)

def json_catch(a, default=None):
    """Fetches the value of a key from the JSON file. If the key doesn't exist, returns a default value."""
    try:
        with open('infos.json', 'r') as fichier:
            data = json.load(fichier)
        return data.get(a, default)  # Using .get() to return the default value if the key doesn't exist
    except FileNotFoundError:
        return default  # If the file doesn't exist, return the default value

def json_update():
    with open('infos.json', 'r') as fichier:
        data = json.load(fichier)
    return data
