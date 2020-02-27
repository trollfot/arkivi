import bjoern
import configparser
from arkivi.emailer import SecureMailer
from arkivi.db import Database
from arkivi.web import Website
from arkivi.api import Backend
from arkivi.request import request
from arkivi.auth import make_jwt_service, protected
from rutter.urlmap import URLMap
from horseman.response import Response


config = configparser.ConfigParser()
config.read('config.ini')


# Preparing the overhead
db = Database(**dict(config.items('db')))
request_factory = request(db)

# Web frontend
emailer = SecureMailer(**dict(config.items('smtp')))
frontend = Website(emailer, request_factory=request_factory)

# API Backend
JWTService = make_jwt_service('jwt.key')
backend = Backend(request_factory=request_factory)

# Creating the main router
application = URLMap(not_found_app=Response.create(404))
application['/'] = frontend
#application['/admin'] = protected(JWTService)(backend)
application['/admin'] = backend

# Serving the app
bjoern.run(application, '0.0.0.0', 9999)
