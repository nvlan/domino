from flask import Blueprint, current_app, send_from_directory

apiref_blueprint = Blueprint('apiref', __name__)

@apiref_blueprint.route('/', methods=('GET',))
def apiref():
    root_dir = current_app.config['STATIC_ROOT']
    return send_from_directory(root_dir, 'apiref.html')
    return "OK", 200
