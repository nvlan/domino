from base import BaseTestCase
from unittest.mock import patch, Mock
from domino.app.libs.r53 import Route53
import json, jwt, os

class RecordsTestCase(BaseTestCase):

    def test_get_records_authenticated_no_data(self):
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers))
        assert response.status_code == 400
        #assert json.loads(response.data.decode("utf-8"))['Error'] == "Missing or wrong data in the request, please check the apiref"

    def test_get_records_authenticated_wrong_data(self):
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {"something": "wrong"}
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 400
        #assert json.loads(response.data.decode("utf-8"))['Error'] == "Missing or wrong data in the request, please check the apiref"

    @patch.object(Route53, "get_records")
    def test_get_records_authenticated_timeout(self, mocked_get_records):
        mocked_get_records.return_value = ['', False]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE'}
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 409

    @patch.object(Route53, "get_records")
    def test_get_records_authenticated_valid_data(self, mocked_get_records):
        mocked_get_records.return_value = ['foobar', True]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE'}
        response = self.client.get('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 200

    def test_create_records_authenticated_wrong_data(self):
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE'}
        response = self.client.post('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 400

    @patch.object(Route53, "action_records")
    def test_create_records_authenticated_valid_data(self, mocked_action_records):
        mocked_action_records.return_value = ['foobar', True]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE',
                    'zone': 'somezone.com',
                    'subdomain': 'something'}
        response = self.client.post('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 200

    @patch.object(Route53, "action_records")
    def test_create_records_authenticated_record_exists(self, mocked_action_records):
        mocked_action_records.return_value = ['foobar', False]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE',
                    'zone': 'somezone.com',
                    'subdomain': 'something'}
        response = self.client.post('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 409

    def test_delete_records_authenticated_wrong_data(self):
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE'}
        response = self.client.delete('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 400

    @patch.object(Route53, "action_records")
    def test_delete_records_authenticated_no_record(self, mocked_action_records):
        mocked_action_records.return_value = ['foobar', False]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE',
                    'zone': 'somezone.com',
                    'subdomain': 'something'}
        response = self.client.delete('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 409

    @patch.object(Route53, "action_records")
    def test_delete_records_authenticated_valid_data(self, mocked_action_records):
        mocked_action_records.return_value = ['foobar', True]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE',
                    'zone': 'somezone.com',
                    'subdomain': 'something'}
        response = self.client.delete('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 200

    def test_patch_records_authenticated_wrong_data(self):
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE'}
        response = self.client.patch('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 400

    @patch.object(Route53, "action_records")
    def test_patch_records_authenticated_valid_data(self, mocked_action_records):
        mocked_action_records.return_value = ['foobar', True]
        token = self.generate_jwt_token('secret')
        self.headers.setdefault('Authorization', 'Bearer ' + token)
        payload = {'id_zone': 'Z000000000000000000NE',
                    'zone': 'somezone.com',
                    'subdomain': 'something',
                    'new_subdomain': 'something-else'}
        response = self.client.patch('/api/domino/records/',
                        headers=(self.headers), data=json.dumps(payload))
        assert response.status_code == 200
