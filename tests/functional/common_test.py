from base import BaseTestCase
import json

class CommonTestCase(BaseTestCase):

    def test_common_health(self):
        response = self.client.get('/api/domino/health/')
        assert response.status_code == 200
