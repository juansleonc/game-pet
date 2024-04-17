from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash
from datetime import datetime, timezone

class User:
    def __init__(self, mongo: PyMongo):
        self.mongo = mongo

    def find_by_email(self, email):
        user = self.mongo.db.users.find_one({"email": email})
        return user if user else None

    def create(self, email, password_hash):
        user_data = {
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now(timezone.utc)
        }
        result = self.mongo.db.users.insert_one(user_data)
        return result.inserted_id

    def verify_password(self, user_id, password):
        user = self.mongo.db.users.find_one({"_id": user_id})
        if user and check_password_hash(user['password_hash'], password):
            return True
        return False
