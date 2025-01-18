from flask import Flask, request, render_template
import json
import updatejson

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        with open('infos.json', 'r') as fichier:
            email = json.load(fichier)
        updatejson.json_edit('name', name)
        updatejson.json_edit('email', email)
        return f"Hello, {name}! We received your email: {email}"
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
