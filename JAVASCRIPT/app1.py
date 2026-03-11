from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/handshake', methods=["GET", "POST"])
# def handshake():
#     python_data = {
#         "message" : "Success! Python is talking to javascript.",
#         "status" : 200
#     }

#     return jsonify(python_data)


patient_db = [
    {"id" : 100, "name" : "Sunny", "age" : 20, "disease" : "Fever"},
    {"id" : 101, "name" : "Aniket", "age" : 18, "disease" : "Fever"},
    {"id" : 102, "name" : "Harsh", "age" : 19, "disease" : "Fever"},
    {"id" : 103, "name" : "Ayush", "age" : 22, "disease" : "Fever"}
]   

@app.route('/', methods=["GET", "POST"])
def home():
    return jsonify({"message" : "Connection established successfully!"})

@app.route('/get_patients', methods=["GET", "POST"])
def get_patients():
    return jsonify(patient_db)

if __name__=='__main__': 
    app.run(debug = True)