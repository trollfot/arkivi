from autoroutes import Routes
from http import HTTPStatus
from pydantic import BaseModel
from horseman.validation import validate
from horseman.meta import APIView, view_methods
from horseman.response import Response as BaseResponse, json, Headers
from horseman.routing import RoutingNode, SentryNode, add_route as route
from horseman.http import HTTPCode

from .db import Collections
from .request import Request


class User(BaseModel):
    username: str
    password: str


class Spectacle(BaseModel):
    id: str
    title: str
    summary: str=''
    presentation: str=''


ROUTER = Routes()


class Response(BaseResponse):

    @classmethod
    def create(cls, code: HTTPCode, body=None, headers: Headers=None):
        status = HTTPStatus(code)
        if headers is None:
            headers = {
                "Access-Control-Allow-Origin": "*"
            }
        elif "Access-Control-Allow-Origin" not in headers:
            headers["Access-Control-Allow-Origin"] = "*"
        return cls(code, body, headers)

    @classmethod
    def from_json(cls, code: HTTPCode, data: str, headers: Headers=None):
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        else:
            headers['Content-Type'] = 'application/json'
        return cls.create(code, body=data, headers=headers)

    @classmethod
    def to_json(cls, code: HTTPCode, body, headers: Headers=None):
        data = json.dumps(body)
        return cls.from_json(code, data, headers=headers)


class Backend(RoutingNode, SentryNode):

    def __init__(self, jwt_service, routes=ROUTER, request_factory=Request):
        self.routes = routes
        self.request_factory = request_factory
        self.jwt_service = jwt_service


class CORSAPIView(APIView):

    def OPTIONS(self, request):
        methods = (name for name, _ in view_methods(self))
        headers = {
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": ",".join(methods),
            "Access-Control-Allow-Headers": (
                "Authorization, Content-Type, X-Requested-With"),
        }
        return Response.create(204, headers=headers)


@route(ROUTER, '/login')
class Login(CORSAPIView):

    def GET(self, request):
        schema = User.schema_json(indent=2)
        return Response.from_json(200, body=schema)

    def check_credentials(self, credentials):
        return (credentials.username == 'admin'
                and credentials.password == 'admin')

    @validate(User)
    def POST(self, request, credentials):
        if not self.check_credentials(credentials):
            return Response.create(403)

        payload = {'user': credentials.username}
        jwt = request.app.jwt_service.generate(payload)
        return Response.to_json(200, {'token': jwt})


@route(ROUTER, '/spectacles')
class SpectaclesAPI(CORSAPIView):

    def GET(self, request):
        if not Collections.SPECTACLES in request.db:
            return Response.to_json(200, [])

        query = f"""FOR spectacle IN {Collections.SPECTACLES.value}
                  RETURN {{
                     id: spectacle._key,
                     title: spectacle.title
                  }}"""

        spectacles = request.db.query(query, rawResults=True)
        return Response.to_json(200, list(spectacles))

    @validate(Spectacle)
    def POST(self, request, new):
        spectacles = request.db.get(Collections.SPECTACLES)
        doc = spectacles.createDocument()
        doc._key = new.id
        doc.set(new.dict())
        doc.save()
        return Response.create(201)


@route(ROUTER, '/spectacles/{spectacle}')
class SpectacleAPI(CORSAPIView):

    def GET(self, request):
        spectacles = request.db.get(Collections.SPECTACLES)
        try:
            doc = spectacles[request.params['spectacle']]
            spectacle = Spectacle(**doc.getStore())
            return Response.from_json(200, spectacle.json())
        except KeyError:
            return Response.create(404)

    @validate(Spectacle)
    def PATCH(self, request, spectacle):
        spectacles = request.db.get(Collections.SPECTACLES)
        try:
            doc = spectacles[request.params['spectacle']]
            doc.set(spectacle.dict())
            doc.save()
            return Response.create(202)
        except KeyError:
            return Response.create(404)

    def DELETE(self, request):
        spectacles = request.db.get(Collections.SPECTACLES)
        try:
            doc = spectacles[request.params['spectacle']]
            doc.delete()
            return Response.create(202)
        except KeyError:
            return Response.create(404)


@route(ROUTER, '/spectacles/{spectacle}/agenda')
class AgendaAPI(CORSAPIView):

    def GET(self, request):
        return Response.create(200)


@route(ROUTER, '/spectacles/{spectacle}/agenda/{date}')
class DateAPI(CORSAPIView):

    def GET(self, request):
        return Response.create(200)

    def PUT(self, request):
        return Response.create(200)

    def PATCH(self, request):
        return Response.create(200)

    def DELETE(self, request):
        return Response.create(200)
