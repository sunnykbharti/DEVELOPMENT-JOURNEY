from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        return jsonify({"message" : "Hello Sunny!"})

class Square(Resource):
    def get(self, num):
        return jsonify({"square" : num**2})

api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')

if __name__ == "__main__":
    app.run(debug=True)