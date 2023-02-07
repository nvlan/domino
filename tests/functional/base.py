import os, unittest, jwt, json
from domino import create_app

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.headers = {'Content-type': 'application/json'}
        os.environ['JWT_TOKEN_SECRET'] = 'c2VjcmV0'

    def generate_jwt_token(self, secret, time=None):
        payload = {'sub': 'tests'}
        if time is not None:
            payload.setdefault('exp', time)
        token_bytes = jwt.encode(payload, secret, algorithm='HS256')
        token = token_bytes.decode('utf-8')
        return token

    def tearDown(self):
        self.app_context.pop()
