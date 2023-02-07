from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.wrappers import Response
from .helpers import get_secret, validate_token
import logging, json

logger = logging.getLogger(__name__)

def authorize(function):
    def wrapper_authorize():
        try:
            token = request.headers['Authorization']
        except:
            resp = Response(
            response=json.dumps({
                'Error': 'Missing authorization header in request'}),
                mimetype='application/json',
                status=400)
            raise BadRequest('Error processing request', response=resp)
        else:
            if token.split()[0] != 'Bearer' or len(token.split()) < 2:
                resp = Response(
                response=json.dumps({
                    'Error': 'Wrong or incomplete token in request'}),
                    mimetype='application/json',
                    status=400)
                raise BadRequest('Error processing request', response=resp)
            secret = get_secret()
            auth_token = token.split()[1]
            result, success = validate_token(auth_token, secret)
            if not success:
                logging.error('Token has issues: ' + result)
                resp = Response(
                response=json.dumps({
                    'message': 'Not Authorized',
                    'reason': result,
                    'error': True}),
                    mimetype='application/json',
                    status=403)
                raise Unauthorized('Error processing request', response=resp)
        return function()
    wrapper_authorize.__name__ = function.__name__
    return wrapper_authorize
