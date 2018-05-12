from apistar import App, Route
from apistar import http
import sys
sys.path.append('../')

import ineko

def getFace(query_params: http.QueryParams) -> dict:
    url = query_params['url']
    re = ineko.recogn_face(url)
    return {
        'response':re
    }

routes = [
    Route('/face', method='GET', handler=getFace),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)