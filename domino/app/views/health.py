from flask import Blueprint, current_app

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/', methods=('GET',))
def health():
    return "Health: OK, Status: Doing good!", 200
