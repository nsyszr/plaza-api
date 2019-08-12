# src/app.py

from flask import Flask
from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt

from .api.organisation import organisation_api as organisation_blueprint
from .api.user import user_api as user_blueprint
from .api.credential import credential_api as credential_blueprint
from .api.account import account_api as account_blueprint

def create_app(env_name):
    # app initiliazation
    app = Flask(__name__)
    CORS(app, resources=r'/api/*')

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    # REST-APIs don't require strict trailing slashed, e.g. /users/
    app.url_map.strict_slashes = False

    app.register_blueprint(organisation_blueprint, url_prefix='/api/v1/organisations')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(credential_blueprint, url_prefix='/api/v1/credentials')
    app.register_blueprint(account_blueprint, url_prefix='/api/v1/accounts')

    @app.route('/', methods=['GET'])
    def index():
        return 'Congratulations! Your first endpoint is workin'

    return app
