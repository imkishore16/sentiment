from flask import Flask,jsonify
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user
from flask_smorest import Blueprint
from Models import *
from flask_smorest import Blueprint
from db import db
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import secrets
# from blocklist import BLOCKLIST
from flask_migrate import Migrate
from controllers.User import blp as userblp
from controllers.Admin import blp as adminblp
from controllers.Temp import blp as tempblp
from controllers.Auth import auth_bp
from flask_cors import CORS

def create_app():
    app=Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True  
    app.config["API_TITLE"] = "Reviews REST API"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    db_url = "postgresql://postgres:root%40123@localhost/reviewsystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)
    CORS(app)
    migrate = Migrate(app, db)
    # jwt = JWTManager(app)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(userblp)
    app.register_blueprint(tempblp) 
    # app.register_blueprint(adminblp) 

    with app.app_context():
        db.create_all()

    
    return app
        

