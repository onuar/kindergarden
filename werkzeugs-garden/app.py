import http.client
import re
import urllib
import urllib.parse
import json
from werkzeug.wrappers import Request, Response

routing_map = {}
last_route_index = -1


@Request.application
def application(request):

    f_url = get_forward_url(request.full_path)
    hostname, port = parse_host_port(f_url) 

    print("route - {} >> {} ".format(request.full_path, f_url))


    f_request_headers = dict(request.headers)

    if request.method == "POST" or request.method == "PUT":
        form_data = list(iterform(request.form))
        form_data = urllib.urlencode(form_data)
        f_request_headers["Content-Length"] = len(form_data)
    else:
        form_data = None

    f_connection = http.client.HTTPConnection(hostname,port)
    f_connection.request(request.method, request.full_path, body=form_data, headers=f_request_headers)
    f_response = f_connection.getresponse()
    
    content = f_response.read()
    status = f_response.status
    content_type = f_response.getheader('content-type')
    
    response = Response(content, status=status, mimetype=content_type, content_type=content_type)
    response.headers.clear()

    for key, value in f_response.getheaders():
        response.headers[key] = value

    return response


def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))

def parse_host_port(h):
    host_port = h.split(":", 1)
    if len(host_port) == 1:
        return (h, 80)
    else:
        host_port[1] = int(host_port[1])
        return host_port

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
