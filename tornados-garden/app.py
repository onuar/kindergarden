from tornado.web import RequestHandler, Application
import tornado.ioloop
import requests
import json


class MainHandler(RequestHandler):
    def get(self):
        self.write("hello main");


class ApiHandler(RequestHandler):
    last_node_index = 0
    nodes = {}

    def initialize(self):
        # nonlocal nodes
        # nonlocal last_node_index

        with open("routing-map-tor.json", "r") as config_file:
            self.nodes = json.load(config_file)

    def get(self):
        self._logging()
        response = self._dispatch("GET")

        self.write("hello api")

    def post(self):
        self._logging()
        response_json = {'name':'onur', 'surname':'aykac'}

        response = self._dispatch("POST")
        self.write({'data':response_json})

    def _logging(self):
        print(self.request.uri)
        print(">>> Headers: "+str(self.request.headers._dict))
        print(">>> Query string parameters: " + str(self.request.arguments))
        print(">>> Body: " + str(self.request.body))
        print("---------")

    def _dispatch(self, method):
        url = self.nodes["nodes"][self.last_node_index]
        internal_response = requests.request(method=method, url=url)

        self.last_node_index += 1

        if self.last_node_index >= self.node["nodes"].length:
            self.last_node_index = 0

        return internal_response


def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/api", ApiHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8081)
    print(">>>   serving on http://localhost:8081   <<<")
    tornado.ioloop.IOLoop.current().start()
