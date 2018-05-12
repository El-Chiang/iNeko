from apistar import App, Route
from apistar import http
import sys
import os
import time
sys.path.append('../')

import ineko

def getFace(query_params: http.QueryParams) -> dict:
    url = query_params['url']
    re = ineko.recogn_face(url)
    return {
        'response':re
    }

def upload_img(request: http.Request) -> dict:
    file_content = bytes(request.body)
    fname = str(time.time())+'.jpg'
    f = open('../uploads/'+fname,'wb')
    f.write(file_content)
    f.close
    if(os.path.exists('../uploads/'+fname)):
        return{
            'response':{
                'url': '../uploads/'+fname
            }
        }
    else:
        return{
            'response':{
                'error': 'upload failed'
            }
        }

routes = [
    Route('/face', method='GET', handler=getFace),
    Route('/images',method='POST',handler=upload_img)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)