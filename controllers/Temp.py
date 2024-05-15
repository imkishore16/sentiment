from flask import Flask, jsonify
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

blp = Blueprint('temp', __name__, description='temp')

@blp.route('/test', methods=['GET'])
def get_status():
    return jsonify({"status": "App is working!"}), 200

