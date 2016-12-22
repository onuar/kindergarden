from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    print(request)
    return Response('Hello World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)