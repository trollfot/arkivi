from pyArango.connection import *

from horseman.parsing import parse
from horseman.routing import RoutingNode, SentryNode
from horseman.response import reply, file_iterator
from horseman.auth import authenticate, BasicAuth
from horseman.meta import Overhead, APIView
from cached_property import cached_property

from .layout import template_endpoint
from .request import Request
from .emailer import SecureMailer, make_email


basic_auth = BasicAuth('Arkivi admin', users={'admin': 'admin'})


class Application(RoutingNode, SentryNode):
    request_type = Request
    configs = None

    @cached_property
    def db(self):
        conn = Connection(
            username=self.configs['db']['user'],
            password=self.configs['db']['password']
        )
        name = self.configs['db']['database']
        if not conn.hasDatabase(name):
            return conn.createDatabase(name)
        return conn[name]


app = Application()


@app.route('/', methods=['GET'])
@template_endpoint('index.pt')
def index(request):
    return {}


@app.route('/spectacles', methods=['GET'])
@template_endpoint('spectacles.pt')
def spectacles(request):
    return {}


@app.route('/tour', methods=['GET'])
@template_endpoint('tournee.pt')
def tournee(request):
    return {}


@app.route('/equipe', methods=['GET'])
@template_endpoint('equipe.pt')
def equipe(request):
    return {}


@app.route('/spectacles/{spectacle}', methods=['GET'])
@template_endpoint('spectacle.pt')
def spectacle(request):
    return {'spectacle': request.params['spectacle']}


@app.route('/admin', methods=['GET'])
@authenticate({"basic": basic_auth}, unauthorized=basic_auth.unauthorized)
def admin(request):
    return reply(body="tu es un admin")


@app.route('/contact')
class Contact(APIView):

    @template_endpoint('contact.pt')
    def GET(self, request):
        return {"sent": False}

    @template_endpoint('contact.pt')
    def POST(self, request):
        if request.content_type:
            form, files = parse(
                request.environ['wsgi.input'], request.content_type)
            data = form.to_dict()

        mailer = SecureMailer(
            request.app.configs['smtp']['host'],
            request.app.configs['smtp']['user'],
            request.app.configs['smtp']['password'],
            int(request.app.configs['smtp']['port']))

        _from = request.app.configs['smtp']['from']
        _to = request.app.configs['smtp']['to']
        mail = make_email(_from, _to, 'contact', data['message'])

        with mailer as sender:
            sender(_from, _to, mail.as_string())

        return {"sent": True}
