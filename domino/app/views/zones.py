from flask import Blueprint
from domino.app.services.zone import get_zone
from domino.app.decorators.decorators import authorize

zones_blueprint = Blueprint('zones', __name__)

@zones_blueprint.route('/', methods=('GET',))
@authorize
def get_zones():
    response, code = get_zone()
    return response, code
