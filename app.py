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


def create_app():
    app=Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True  
    app.config["API_TITLE"] = "Stores REST Api"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" 
    
    # db_url = "postgresql://postgres:root%40123@localhost/ordering"
    app.config["SQLALCHEMY_DATABASE_URI"] = "db_url" or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    api = Api(app)
    migrate = Migrate(app, db)  
    with app.app_context():
        db.create_all()
    jwt = JWTManager(app)

    auth_bp = Blueprint('auth', __name__, description='auth')

    @auth_bp.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    @auth_bp.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    # Register blueprints and error handlers
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.before_first_request
    def create_tables():
        db.create_all()
        
    return app








    









        


     