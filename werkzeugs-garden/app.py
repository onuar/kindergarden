import http.client
import urllib
import urllib.parse
import json
from werkzeug.wrappers import Request, Response

port = 9999
routing_map = {}
last_route_index = -1


@Request.application
def application(request):
    response = forward_request(request)
    return response


def forward_request(request):
    f_response = proxy_request(request)   
    content = f_response.read()
    status = f_response.status
    content_type = f_response.getheader('content-type')
    
    response = Response(content, status=status, content_type=content_type)    
    response.headers.clear()

    for key, value in f_response.getheaders():
        response.headers[key] = value

    return response


def proxy_request(request):
    f_host = get_forward_host()
    print("route - {} >> {} ".format(request.full_path, f_host))

    f_request_headers = dict(request.headers)
    
    if request.method == "POST" or request.method == "PUT":
        form_data = list(iterform(request.form))
        form_data = urllib.parse.urlencode(form_data)
        f_request_headers["Content-Length"] = len(form_data)
    else:
        form_data = None

    f_connection = http.client.HTTPConnection(f_host)
    f_connection.request(request.method, request.full_path, body=form_data, headers=f_request_headers)
    f_response = f_connection.getresponse()
    return f_response


def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))

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
    url = routing_map["nodes"][next_route_index]
    if request_path != None:
         url = url + "" + request_path
    return url

def get_forward_host():
    next_route_index = get_next_route_index()
    url = routing_map["nodes"][next_route_index]
    return url


if __name__ == '__main__':
    with open('routing-map.json') as json_data:
        routing_map = json.load(json_data)

    from werkzeug.serving import run_simple
    run_simple('localhost', port, application, use_reloader=True, threaded=True)
