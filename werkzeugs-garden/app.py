import json
import requests
from werkzeug.wrappers import Request, Response

routing_map = {}
last_route_index = -1


@Request.application
def application(request):
    print(request.full_path)
    # print(routing_map["nodes"])

    forward_url = get_forward_url(request.full_path)
    print("route -> ", forward_url)

    f_response = requests.request(
        request.method, forward_url, data=request.data, headers=request.headers)

    response = Response(f_response.content)
    response.headers.clear()

    for key, value in f_response.headers.items():
        response.headers[key] = value

    return response


def get_next_route_index():
    global last_route_index
    length = len(routing_map["nodes"])
    next_route_index = last_route_index + 1

    if next_route_index == length:
        next_route_index = 0

    last_route_index = next_route_index
    return next_route_index


def get_forward_url(request_path):
    next_route_index = get_next_route_index()
    return routing_map["nodes"][next_route_index] + "" + request_path


if __name__ == '__main__':
    with open('routing-map.json') as json_data:
        routing_map = json.load(json_data)

    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)
