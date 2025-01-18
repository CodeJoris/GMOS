from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_variable', methods=['GET'])
def get_variable():
    # La variable à renvoyer
    my_variable = "Bonjour, voici la variable Python!"
    return jsonify({"variable": my_variable})

if __name__ == '__main__':
    app.run(debug=True)
