import json
import requests
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    print(request.full_path)

    with open('routing-map.json') as json_data:
        routing_map = json.load(json_data)

    print(routing_map["nodes"])

    

    response = Response('rıytşb')
    return response

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)


class Nodes(object):
    order int
    url str
    def __init__(self, url):
        self.name = name
        self.username = username