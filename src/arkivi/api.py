from autoroutes import Routes
from pydantic import BaseModel

from horseman.validation import validate
from horseman.meta import APIView, view_methods
from horseman.response import reply, json_reply
from horseman.routing import RoutingNode, SentryNode, add_route as route
from .request import Request


class User(BaseModel):
    username: str
    password: str


ROUTER = Routes()


class Backend(RoutingNode, SentryNode):

    def __init__(self, jwt_service, routes=ROUTER, request_factory=Request):
        self.routes = routes
        self.request_factory = request_factory
        self.jwt_service = jwt_service


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


@route(ROUTER, '/login')
class Login(CORSAPIView):

    def GET(self, request):
        schema = User.schema_json(indent=2)
        return reply(
            body=schema, headers={'Content-Type': "application/json"})

    def check_credentials(self, credentials):
        return (credentials.username == 'admin'
                and credentials.password == 'admin')

    @validate(User)
    def POST(self, request, credentials):
        if not self.check_credentials(credentials):
            return reply(403)

        payload = {'user': credentials.username}
        jwt = request.app.jwt_service.generate(payload)
        return json_reply(body={'token': jwt})


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
