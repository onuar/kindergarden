import tornado.ioloop
import json

from tornado.web import RequestHandler, Application
from tornado.httpclient import HTTPRequest, AsyncHTTPClient


class EntryPoint(RequestHandler):
    last_node_index = 0
    nodes = {}

    def initialize(self):
        with open("routing-map-tor.json", "r") as config_file:
            self.nodes = json.load(config_file)

    @tornado.web.asynchronous
    def get(self):
        self.write_log()
        self.dispatch_internal(response_callback=self.response_handler)

    def post(self):
        self.write_log()
        self.dispatch_internal(response_callback=self.response_handler)

    def response_handler(self, response):
        self.set_status(response.code)
        self._headers = tornado.httputil.HTTPHeaders()

        for header, v in response.headers.get_all():
            if header not in ('Content-Length', 'Transfer-Encoding', 'Content-Encoding', 'Connection'):
                self.add_header(header, v)

        if response.body:
            self.set_header('Content-Length', len(response.body))
            self.write(response.body)

        self.finish()

    def dispatch_internal(self, response_callback):
        url = self.get_node()
        body = self.request.body
        if not body:
            body = None
        if self.request.path:
            url = url + self.request.path

        request = HTTPRequest(url=url, headers=self.request.headers, method=self.request.method, body=body)
        client = AsyncHTTPClient()
        client.fetch(request, response_callback)

    def get_node(self):
        url = self.nodes["nodes"][EntryPoint.last_node_index]
        EntryPoint.last_node_index += 1

        if EntryPoint.last_node_index >= len(self.nodes["nodes"]):
            EntryPoint.last_node_index = 0

        print(url)
        return url

    def write_log(self):
        print("{} {}".format(self.request.method, self.request.uri))


def make_app():
    return Application([
        (r'.*', EntryPoint)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8081)
    print(">>>   serving on http://localhost:8081   <<<")
    tornado.ioloop.IOLoop.current().start()
