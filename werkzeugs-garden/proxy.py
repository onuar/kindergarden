import http.client
import urllib
import urllib.parse
from urllib.parse import urlparse
import json
from werkzeug.wrappers import Request, Response

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
    target_url = request.values["url"]
    url_scheme = urlparse(target_url)
    f_host = url_scheme.hostname
    
    print("proxy - {} ".format(f_host))

    f_request_headers = dict(request.headers)
    f_request_headers.pop('Host',None)

    if request.method == "POST" or request.method == "PUT":
        form_data = list(iterform(request.form))
        form_data = urllib.parse.urlencode(form_data)
        f_request_headers["Content-Length"] = len(form_data)
    else:
        form_data = None

    if url_scheme.scheme == "https":
        f_connection = http.client.HTTPSConnection(f_host)
    else:
        f_connection = http.client.HTTPConnection(f_host)
    
    f_connection.request(request.method, url_scheme.path, body=form_data, headers=f_request_headers)
    f_response = f_connection.getresponse()
    return f_response


def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))


def get_forward_host():
    next_route_index = get_next_route_index()
    url = routing_map["nodes"][next_route_index]
    return url


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8008, application)
