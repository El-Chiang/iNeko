from flask import Flask,jsonify,request,Response,Request
from flask_restful import Resource, Api,reqparse

import sys
sys.path.append('../')

import ineko

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('content')

class Face(Resource):
    def get(self):
        
        args = parser.parse_args()
        url = args['url']
        re = ineko.recogn_face(url)
        return {
            'response':re
        }

class image(Resource):
    def post(self):
        return {
            "1":request.values
        }

api.add_resource(Face, '/face')
api.add_resource(image, '/images')

if __name__ == '__main__':
    app.run(debug=True)
    