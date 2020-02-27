import json
from pathlib import Path
from functools import wraps
from jwcrypto import jwk
from horseman.response import Response
from cromlech.jwt.components import TokenException, JWTHandler, JWTService


def get_key(path: Path):
    if not path.is_file():
        with open(path, 'w+', encoding="utf-8") as keyfile:
            key = JWTHandler.generate_key()
            export = key.export()
            keyfile.write(export)
    else:
        with open(path, 'r', encoding="utf-8") as keyfile:
            data = json.loads(keyfile.read())
            key = jwk.JWK(**data)

    return key


def make_jwt_service(key, TTL=600):
    key = get_key(Path(key))
    return JWTService(key, JWTHandler, lifetime=TTL)


def protected(jwt_service):

    unauthorized = Response.create(401)

    def jwt_protection(wrapped):
        @wraps(wrapped)
        def check_token(environ, start_response):
            auth = environ.get('HTTP_AUTHORIZATION')
            if auth:
                authtype, token = auth.split(' ', 1)
                if authtype.lower() == 'bearer':
                    try:
                        payload = jwt_service.check_token(token)
                    except (TokenException, ValueError) as err:
                        payload = None
                    if payload is not None:
                        return wrapped(environ, start_response)
            return unauthorized(environ, start_response)
        return check_token

    return jwt_protection
