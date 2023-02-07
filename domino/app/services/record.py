from flask import current_app
from domino.app.libs.r53 import Route53
import json
from flask import request

error_aws = { 'Error' : 'Problem communicating with AWS, please try again later' }
error_data = { 'Error' : 'Missing or wrong data in the request, please check the apiref'}
record_update = { 'Success' : 'The record has been updated' }
def get_record(data=None):
    if data is None or 'id_zone' not in data:
        return error_data, 400
    else:
        r53 = Route53(current_app, data)
        records, success = r53.get_records()
        if success:
            return records, 200
        else:
            return records, 409

def create_record(data=None):
    if data is None or 'id_zone' not in data or 'zone' not in data or 'subdomain' not in data:
        return error_data, 400
    else:
        data['action'] = 'CREATE'
        r53 = Route53(current_app, data)
        message, success = r53.action_records()
    if success:
        return message, 200
    else:
        return message, 409

def delete_record(data=None):
    if data is None or 'id_zone' not in data or 'zone' not in data or 'subdomain' not in data:
        return error_data, 400
    else:
        data['action'] = 'DELETE'
        r53 = Route53(current_app, data)
        message, success = r53.action_records()
    if success:
        return message, 200
    else:
        return message, 409

def patch_record(data=None):
    if data is None or 'id_zone' not in data or 'zone' not in data or 'subdomain' not in data or 'new_subdomain' not in data:
        return error_data, 400
    else:
        data['action'] = 'DELETE'
        r53 = Route53(current_app, data)
        r53.action_records()
        data['action'] = 'CREATE'
        data['update'] = 'True'
        data['subdomain'] = data['new_subdomain']
        r53 = Route53(current_app, data)
        message, success = r53.action_records()
        if success:
            return message, 200
        else:
            return message, 409
