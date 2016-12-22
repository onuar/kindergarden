from tornado.web import RequestHandler, Application
import tornado.ioloop


class MainHandler(RequestHandler):
    def get(self):
        self.write("hello main");


class ApiHandler(RequestHandler):
    def get(self):
        self._logging()
        self.write("hello api")

    def post(self):
        self._logging()
        response_json = {'name':'onur', 'surname':'aykac'}
        self.write({'data':response_json})

    def _logging(self):
        print(self.request.uri)
        print(">>> Headers: "+str(self.request.headers._dict))
        print(">>> Query string parameters: " + str(self.request.arguments))
        print(">>> Body: " + str(self.request.body))
        print("---------")

    def _internal_call(self):
        pass


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

