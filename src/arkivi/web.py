"""
ARKIVI Website
"""
from pyArango import theExceptions
from autoroutes import Routes

from horseman.meta import APIView
from horseman.parsing import parse
from horseman.routing import RoutingNode, SentryNode, add_route as route

from .db import Collections
from .layout import template_endpoint
from .request import Request


ROUTER = Routes()


class Website(RoutingNode, SentryNode):

    __slots__ = ('routes', 'emailer', 'storage', 'request_factory')

    def __init__(self, emailer, storage, request_factory=Request):
        self.routes = ROUTER
        self.emailer = emailer
        self.storage = storage
        self.request_factory = request_factory


@route(ROUTER, '/', methods=['GET'])
@template_endpoint('index.pt')
def index(request):
    return {}


@route(ROUTER, '/spectacles', methods=['GET'])
@template_endpoint('spectacles.pt')
def spectacles(request):
    query = f"""FOR spectacle IN {Collections.SPECTACLES.value}
                  RETURN {{
                     id: spectacle._key,
                     title: spectacle.title,
                     description: spectacle.description
                  }}"""
    spectacles = request.db.query(query, rawResults=True)
    return { 'spectacles': list(spectacles) }


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
    spectacles = request.db.get(Collections.SPECTACLES)
    try:
        return {
            'spectacle': spectacles[request.params['spectacle']]
        }
    except theExceptions.DocumentNotFoundError:
        raise KeyError


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
