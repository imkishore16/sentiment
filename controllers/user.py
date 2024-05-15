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
from Mlmodel.predict import predict_sentiment




blp = Blueprint("user",__name__,description="user side Api's")

@blp.route('/api/movies/<string:movie_name>/reviews')
def get_movie_reviews(movie_name):
    movie = Movie.query.filter_by(name=movie_name).first_or_404()
    reviews = Review.query.filter_by(movie_id=movie.id).all()

    review_schema = ReviewSchema(many=True)
    serialized_reviews = review_schema.dump(reviews)

    return jsonify(serialized_reviews), 200

# @blp.route('/get-user', meth
@blp.route('/testing', methods=['POST'])
def get_status():
    return jsonify({"status": "App is working!"}), 200



@blp.route('/api/movies/<string:movie_name>/reviews', methods=['POST'])
def create_movie_review(movie_name):
    movie = Movie.query.filter_by(name=movie_name).first_or_404()

    review_data = request.get_json()
    review_text = review_data.get('review')
    # // call the sentiment ml model
    print(review_text)
    sentiment = predict_sentiment(review_text)

    if not review_text or not sentiment:
        return jsonify({'error': 'Both review and sentiment are required'}), 400

    new_review = Review(review=review_text, sentiment=sentiment)
    new_review.movie_id = movie.id
    db.session.add(new_review)
    db.session.commit()

    serialized_review = ReviewSchema().dump(new_review)
    return jsonify(serialized_review), 200


@blp.route('/api/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        return jsonify({'error': 'You are not authorized to update this review'}), 403

    review_schema = ReviewSchema()
    review_data = request.get_json()

    try:
        updated_review = review_schema.load(review_data, instance=review, partial=True)
    except Exception as err:
        return jsonify({'errors': err.messages}), 400

    db.session.commit()

    serialized_review = review_schema.dump(updated_review)
    return jsonify(serialized_review), 200