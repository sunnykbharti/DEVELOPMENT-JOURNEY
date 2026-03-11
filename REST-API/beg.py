from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#defining a simple resource
class Sunny(Resource):
    def get(self):
        return {"message" : "Hello World!"}

# Add resource to Api
api.add_resource(Sunny, '/')

if __name__ == '__main__':
    app.run(debug=True)