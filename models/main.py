"""DB Object and Models for ORM"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Users table model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User: (id: {self.id}, name: {self.name})"


class Movie(db.Model):
    """Movies table model"""
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)
    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref='movies', foreign_keys=[user_id])

    def __repr__(self):
        return (f"Movie: (id: {self.id}, title: {self.name},"
                f" year: {self.year}, director: {self.director})")
