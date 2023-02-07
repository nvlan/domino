from flask import current_app
from domino.app.libs.r53 import Route53
import json

error_msg = { 'Error' : 'Problem communicating with AWS, please try again later' }
def get_zone():
    r53 = Route53(current_app)
    zones, success = r53.get_all_zones()
    if success:
        return zones, 200
    else:
        return error_msg, 500
