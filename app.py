import bjoern
import configparser
from pathlib import Path
from arkivi.emailer import SecureMailer
from arkivi.db import Database
from arkivi.web import Website
from arkivi.api import Backend
from arkivi.storage import Storage
from arkivi.request import request
from arkivi.auth import make_jwt_service, jwt_protection
from rutter.urlmap import URLMap
from horseman.response import Response


current = Path(__file__).parent

config = configparser.ConfigParser()
config.read(current / 'config.ini')

# Storage config
storage = Storage(**dict(config.items('storage')))

# Preparing the overhead
db = Database(**dict(config.items('db')))
request_factory = request(db)

# Web frontend
emailer = SecureMailer(**dict(config.items('smtp')))
frontend = Website(emailer, storage, request_factory=request_factory)

# API Backend
JWTService = make_jwt_service(current / 'jwt.key')
backend = Backend(JWTService, storage, request_factory=request_factory)

# Creating the main router
application = URLMap(not_found_app=Response.create(404))
application['/'] = frontend
application['/admin'] = jwt_protection(backend, excludes=['/login'])

# Serving the app
bjoern.run(application, 'unix:/tmp/bjoern.sock')
