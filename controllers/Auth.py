from flask import Flask ,request
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user
from db import db
import uuid
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from flask import jsonify

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy import not_
from flask_jwt_extended import jwt_required, current_user

from Models import *
from Schemas import *
from Exception import CustomException
from flask import jsonify, request

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