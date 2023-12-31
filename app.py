import os
import secrets
from flask import Flask, jsonify
from flask_smorest import Api
from db import db
import Models #this is the __init__.py file in the Models folder
from Resources.item import blp as ItemBlueprint
from Resources.store import blp as StoreBlueprint
from Resources.tag import blp as TagBlueprint
from Resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db") #temp until we migrate to postgres
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_DEBUG"] = True
    db.init_app(app)
    migrate = Migrate(app, db)

    app.config["JWT_SECRET_KEY"] = "10155051890371939519"
    jwt = JWTManager(app)
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401




    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app;




