from flask import Flask,request
from flask_restful import Resource, Api,reqparse
import time

import sys
sys.path.append('../')

import ineko
import pymysql

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

class cats(Resource):
    def get(self):
        db = pymysql.connect("139.198.4.68","root","iNeko2018","ineko" )
        cursor = db.cursor()
        sql = 'select * from cats'
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        return{
            'data':data
        }
    def post(self):
        args = parser.parse_args()
        parser.add_argument('name')
        parser.add_argument('img')
        parser.add_argument('data')
        name = args['name']
        img = args['img']
        data = args['data']
        db = pymysql.connect("139.198.4.68","root","iNeko2018","ineko" )
        cursor = db.cursor()
        sql = "insert into cats (name,img,data) values ('"+ name + "','" + img + "','" + data  +"')"
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return {
                'response':{
                    'message':'success'
                }
            }
        except:
            db.rollback()
            return {
                'response':{
                    'message':'faild'
                }
            }

    
class cat(Resource):
    def get(self,cat_id):
        db = pymysql.connect("139.198.4.68","root","iNeko2018","ineko" )
        cursor = db.cursor()
        sql = 'select * from cats where id = ' + cat_id
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        return{
            'data':data
        }


api.add_resource(Face, '/face')
api.add_resource(image, '/images')
api.add_resource(cats,'/cats')
api.add_resource(cat,'/cats/<cat_id>')

if __name__ == '__main__':
    app.run(debug=True)
    