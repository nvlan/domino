from flask import Flask
from domino.app.views.health import health_blueprint
from domino.app.views.apiref import apiref_blueprint
from domino.app.views.zones import zones_blueprint
from domino.app.views.records import records_blueprint
from domino.app.views.root import proxy_route
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def create_app():
    # create application instance
    app = Flask(__name__)
    app.config.from_object('domino.config.settings')
    app.wsgi_app = DispatcherMiddleware(proxy_route, {app.config['PREFIX_APP_URL']: app.wsgi_app})
    app.register_blueprint(health_blueprint, url_prefix='/health')
    app.register_blueprint(zones_blueprint, url_prefix='/zones')
    app.register_blueprint(records_blueprint, url_prefix='/records')
    app.register_blueprint(apiref_blueprint, url_prefix='/apiref')
    return app
