from autoroutes import Routes

from horseman.meta import APIView, view_methods
from horseman.response import reply
from horseman.routing import RoutingNode, SentryNode, add_route as route
from .request import Request


ROUTER = Routes()


class Backend(RoutingNode, SentryNode):

    def __init__(self, routes=ROUTER, request_factory=Request):
        self.routes = routes
        self.request_factory = request_factory


class CORSAPIView(APIView):

    def OPTIONS(self, request):
        methods = (name for name, _ in view_methods(self))
        headers = {
            "Access-Control-Allow-Origin": request.headers.get('Origin'),
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": ",".join(methods),
            "Access-Control-Allow-Headers": (
                "Authorization, Content-Type, X-Requested-With"),
        }
        return reply(204, headers=headers)


@route(ROUTER, '/spectacles')
class Spectacles(CORSAPIView):

    def GET(self, request):
        return reply(200)


@route(ROUTER, '/spectacles/{spectacle}')
class Spectacle(CORSAPIView):

    def GET(self, request):
        return reply(200)

    def PUT(self, request):
        return reply(200)

    def PATCH(self, request):
        return reply(200)

    def DELETE(self, request):
        return reply(200)


@route(ROUTER, '/spectacles/{spectacle}/agenda')
class Agenda(CORSAPIView):

    def GET(self, request):
        return reply(200)


@route(ROUTER, '/spectacles/{spectacle}/agenda/{date}')
class Date(CORSAPIView):

    def GET(self, request):
        return reply(200)

    def PUT(self, request):
        return reply(200)

    def PATCH(self, request):
        return reply(200)

    def DELETE(self, request):
        return reply(200)
