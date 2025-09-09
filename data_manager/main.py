"""DataManager for CRUD operations"""
from models import db, User, Movie

class DataManager():
    """Handles CRUD operations with static methods"""
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()