from horseman.meta import Overhead


class Request(Overhead):

    __slots__ = (
        'app', 'db', 'environ', 'params', 'data', 'method', 'content_type'
    )

    def __init__(self, db, app, environ, **params):
        self.db = db
        self.app = app
        self.environ = environ
        self.params = params
        self.data = {}
        self.method = environ['REQUEST_METHOD']
        if self.method in ('POST', 'PATCH', 'PUT'):
            self.content_type = environ.get(
                'CONTENT_TYPE', 'application/x-www-form-urlencoded')
        else:
            self.content_type = None

    def set_data(self, data):
        self.data = data


def request(db):
    def factory(app, environ, **args):
        return Request(db, app, environ, **args)
    return factory
