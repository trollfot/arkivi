import bjoern
from horseman.routing import RoutingNode, SentryNode
from horseman.response import reply
from horseman.auth import authenticate, BasicAuth
from horseman.meta import Overhead, APIView
from chameleon.zpt.template import PageTemplateFile


class Request(Overhead):

    __slots__ = (
        'environ', 'params', 'data', 'method', 'content_type'
    )

    def __init__(self, environ, **args):
        self.environ = environ
        self.params = args
        self.data = {}
        self.method = environ['REQUEST_METHOD']
        if self.method in ('POST', 'PATCH', 'PUT'):
            self.content_type = environ.get(
                'CONTENT_TYPE', 'application/x-www-form-urlencoded')
        else:
            self.content_type = None

    def set_data(self, data):
        self.data = data


class Application(RoutingNode, SentryNode):
    request_type = Request


app = Application()


class Layout:

    def __init__(self, path, **namespace):
        self._template = PageTemplateFile(path)
        self._namespace = namespace

    def __call__(self, template, **extra):
        ns = {**self._namespace, **extra}
        content = template.render(**ns)
        return self._template.render(content=content, **ns)


layout = Layout('layout.pt')
basic_auth = BasicAuth('Arkivi admin', users={'admin': 'admin'})


@app.route('/', methods=['GET'])
def index(request):
    template = PageTemplateFile('index.pt')
    return reply(body=layout(template))


@app.route('/spectacles/', methods=['GET'])
def spectacles(request):
    template = PageTemplateFile('spectacles.pt')
    return reply(body=layout(template))


@app.route('/spectacles/{spectacle}', methods=['GET'])
def spectacle(request):
    template = PageTemplateFile('spectacle.pt')
    return reply(body=layout(template, **request.params))


@app.route('/admin', methods=['GET'])
@authenticate({"basic": basic_auth}, unauthorized=basic_auth.unauthorized)
def admin(request):
    template = PageTemplateFile('index.pt')
    return reply(body=layout(template))



bjoern.run(app, '127.0.0.1', 8080)
