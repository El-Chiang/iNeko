from flask import Flask
from flask_restful import Resource, Api,reqparse
import time

import sys
sys.path.append('../')

import ineko

site_url = '127.0.0.1'

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class Face(Resource):
    def get(self):
        args = parser.parse_args()
        parser.add_argument('url')
        url = args['url']
        re = ineko.recogn_face(url)
        return {
            'response':re
        }

class image(Resource):
    
    def post(self):
        args = parser.parse_args()
        parser.add_argument('content')
        content = bytes(args['content'],'utf-8')
        fname = str(time.time())+'.jpg'
        f = open('../uploads/'+fname,'wb')
        f.write(content)
        f.close
        return {
            'response':{
                'url':site_url+'/uploads/'+fname
            }
        }

api.add_resource(Face, '/face')
api.add_resource(image, '/images')

if __name__ == '__main__':
    app.run(debug=True)
    