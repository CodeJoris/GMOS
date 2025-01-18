from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/run-python', methods=['GET'])
def run_python():
    # Ici, vous pouvez exécuter votre code Python
    result = "Résultat de l'exécution de Python"
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)