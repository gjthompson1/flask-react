# app/__init__.py

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from app.api.ping import ping_blueprint
    from app.api.users import users_blueprint
    from app.api.roles import roles_blueprint

    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(roles_blueprint)

    return app
