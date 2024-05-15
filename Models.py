
# from db import db
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)

#     # Zero to many relationship between User and Review
#     reviews = db.relationship('Review', backref='user', lazy=True)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class Review(db.Model):
#     __tablename__ = 'reviews'
#     id = db.Column(db.Integer, primary_key=True)
#     review = db.Column(db.Text, nullable=False)
#     sentiment = db.Column(db.String, nullable=False)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable to allow zero reviews for a user

#     # Relationships
#     movie = db.relationship('Movie', backref=db.backref('reviews', lazy=True))


# class Movie(db.Model):
#     __tablename__ = 'movies'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)

#     # One-to-many relationship between Movie and Review
#     reviews = db.relationship('Review', backref='movie', lazy=True)

from db import db
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One-to-many relationship between Movie and Review
    reviews = db.relationship('Review', backref='movie', lazy=True)
