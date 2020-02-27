"""
ARKIVI Website
"""
from autoroutes import Routes

from horseman.meta import APIView
from horseman.parsing import parse
from horseman.routing import RoutingNode, SentryNode, add_route as route

from .db import Collections
from .layout import template_endpoint
from .request import Request


ROUTER = Routes()


class Website(RoutingNode, SentryNode):

    def __init__(self, emailer, routes=ROUTER, request_factory=Request):
        self.routes = routes
        self.emailer = emailer
        self.request_factory = request_factory


@route(ROUTER, '/', methods=['GET'])
@template_endpoint('index.pt')
def index(request):
    return {}


@route(ROUTER, '/spectacles', methods=['GET'])
@template_endpoint('spectacles.pt')
def spectacles(request):
    spectales = request.db.get(Collections.SPECTACLES)
    return {
        'spectacles': [spectacle for spectacle in spectales.fetchAll()]
    }


@route(ROUTER, '/tour', methods=['GET'])
@template_endpoint('tournee.pt')
def tournee(request):
    return {}


@route(ROUTER, '/equipe', methods=['GET'])
@template_endpoint('equipe.pt')
def equipe(request):
    return {}


@route(ROUTER, '/spectacles/{spectacle}', methods=['GET'])
@template_endpoint('spectacle.pt')
def spectacle(request):
    return {'spectacle': request.params['spectacle']}


@route(ROUTER, '/contact')
class Contact(APIView):

    @template_endpoint('contact.pt')
    def GET(self, request):
        return {"sent": False}

    @template_endpoint('contact.pt')
    def POST(self, request):
        form, files = parse(
            request.environ['wsgi.input'], request.content_type)
        data = form.to_dict()
        mail = request.app.emailer.email('contact', data['message'])
        with request.app.emailer.smtp() as sender:
            sender(mail.as_string())

        return {"sent": True}
