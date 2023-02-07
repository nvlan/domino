from flask import Blueprint, request
from domino.app.services.record import get_record, patch_record, create_record, delete_record
from domino.app.decorators.decorators import authorize

records_blueprint = Blueprint('records', __name__)

@records_blueprint.route('/', methods=('GET',))
@authorize
def get_records():
    data = request.json
    response, code = get_record(data)
    return response, code

@records_blueprint.route('/', methods=('POST',))
@authorize
def create_records():
    data = request.json
    response, code = create_record(data)
    return response, code

@records_blueprint.route('/', methods=('DELETE',))
@authorize
def delete_records():
    data = request.json
    response, code = delete_record(data)
    return response, code


@records_blueprint.route('/', methods=('PATCH',))
@authorize
def patch_records():
    data = request.json
    response, code = patch_record(data)
    return response, code
