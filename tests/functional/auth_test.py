from base import BaseTestCase
from unittest.mock import patch, Mock
from domino.app.libs.r53 import Route53
import json

class AuthTestCase(BaseTestCase):

    def test_auth_unauthenticated(self):
        response = self.client.get('/api/domino/zones/')
        assert response.status_code == 400
        assert json.loads(response.data.decode("utf-8"))['Error'] == 'Missing authorization header in request'

    def test_auth_wrong_auth_type(self):
        self.headers.setdefault('Authorization', 'Basic foobar')
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers))
        assert response.status_code == 400
        assert json.loads(response.data.decode("utf-8"))['Error'] == 'Wrong or incomplete token in request'

    def test_auth_wrong_token(self):
        token = self.generate_jwt_token('badsecret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        response = self.client.get('/api/domino/zones/',
                        headers=(self.headers))
        assert response.status_code == 403
        assert json.loads(response.data.decode("utf-8"))['reason'] == 'Invalid token'

    def test_auth_expired_token(self):
        token = self.generate_jwt_token('secret', 1602817663)
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers))
        assert response.status_code == 403
        assert json.loads(response.data.decode("utf-8"))['reason'] == 'Signature expired'
