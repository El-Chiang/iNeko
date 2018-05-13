from flask import Flask,request
from flask_restful import Resource, Api,reqparse
import time

import sys
sys.path.append('../')

import ineko
import pymysql

site_url = '127.0.0.1'
db_ip = '139.198.4.68'
db_user = 'root'
db_password = 'iNeko2018'
db_name = 'ineko'

def db_get(sql):
    db = pymysql.connect(db_ip,db_user,db_password,db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def db_post(sql):
    db = pymysql.connect(db_ip,db_user,db_password,db_name)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

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
            'response':{
                'face':re
            }
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
        sql = 'select * from cats'
        data = db_get(sql)
        return{
            'response':{
                'cats_list':data
            }
        }
    def post(self):
        args = parser.parse_args()
        parser.add_argument('name')
        parser.add_argument('img')
        parser.add_argument('data')
        name = args['name']
        img = args['img']
        data = args['data']
        sql = "insert into cats (name,img,data) values ('"+ name + "','" + img + "','" + data  +"')"
        if(db_post(sql)):
            return {
                'response':{
                    'message':'success'
                }
            }
        else:
            return {
                'response':{
                    'message':'faild'
                }
            }
    
class cat(Resource):
    def get(self,cat_id):
        sql = 'select * from cats where id = ' + cat_id
        data = db_get(sql)
        return{
            'response':{
                'cat_info':data
            }
        }

class cat_data(Resource):
    def get(self,cat_id):
        sql = 'select data from cats_data where cat = ' + cat_id
        data = db_get(sql)
        return{
            'response':{
                'cat_datas':data
            }
        }

class cats_data(Resource):
    def get(self):
        sql = 'select cat,data from cats_data'
        data = db_get(sql)
        return{
            'response':{
                'cats_datas':data
            }
        }

class identify(Resource):
    def get(self):
        args = parser.parse_args()
        parser.add_argument('url')
        url = args['url']
        if(url=='Cat_3.jpg'):
            return {
                'response':{
                        'id':2,
                        'cat':'tiecha'
                    }
            }
        else:
            return {
                'response':{
                        'id':1,
                        'cat':'pipi'
                    }
            }


api.add_resource(Face, '/face')
api.add_resource(image, '/images')
api.add_resource(cats,'/cats')
api.add_resource(cat,'/cats/<cat_id>')
api.add_resource(cat_data,'/cats_data/<cat_id>')
api.add_resource(cats_data,'/cats_data')
api.add_resource(identify,'/identify')

if __name__ == '__main__':
    app.run(debug=True)
    