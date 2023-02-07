from werkzeug.serving import run_simple
from flask import current_app


def proxy_route(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Wrong path, please check the apiref']
