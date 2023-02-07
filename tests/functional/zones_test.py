from base import BaseTestCase
from unittest.mock import patch, Mock
from domino.app.libs.r53 import Route53
import json

class ZonesTestCase(BaseTestCase):

    @patch.object(Route53, "get_all_zones")
    def test_zone_authenticated(self, mocked_get_all_zones):
        mocked_get_all_zones.return_value = ['foobar', True]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        response = self.client.get('/api/domino/zones/',
                        headers=(self.headers))
        assert response.status_code == 200

    @patch.object(Route53, "get_all_zones")
    def test_zone_authenticated_timeout(self, mocked_get_all_zones):
        mocked_get_all_zones.return_value = ['', False]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        response = self.client.get('/api/domino/zones/',
                        headers=(self.headers))
        assert response.status_code == 500
        assert json.loads(response.data.decode("utf-8"))['Error'] == 'Problem communicating with AWS, please try again later'
