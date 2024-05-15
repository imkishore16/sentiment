from flask import Flask ,request
from datetime import datetime
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
from Mlmodel.predict import *

blp = Blueprint("admin",__name__,description="admin side Api's")
@blp.route('/api/movies', methods=['POST'])
def post_movie():
    movie_data = request.get_json()
    
    name = movie_data.get('name')
    
    if not name:
        return jsonify({"error": "Name is a required field."}), 400
    
    new_movie = Movie(name=name)
    
    try:
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({"message": "Movie added successfully!", "movie": {"id": new_movie.id, "name": new_movie.name}}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

