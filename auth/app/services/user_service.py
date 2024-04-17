from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.services.auth_service import AuthService
import os

class UserService:
    def __init__(self):
        self.auth_service = AuthService(secret_key=os.getenv('SECRET_KEY'))
        self.user_model = None

    def set_mongo(self, mongo):
        self.user_model = User(mongo) 
        
    def authenticate_user(self, email, password):
        user = self.user_model.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            token = self.auth_service.generate_token(user.id)
            return token, None
        return None, "Invalid email or password"

    def create_user(self, email, password):
        existing_user = self.user_model.find_by_email(email)
        if existing_user:
            return None, "User already exists"

        password_hash = generate_password_hash(password)
        new_user_id = self.user_model.create(email, password_hash)
        return new_user_id, None

    def initiate_password_reset(self, email):
        user = self.user_model.find_by_email(email)
        if not user:
            return "User not found", 404

        # Assume we have a method to generate a password reset token
        reset_token = self.auth_service.generate_password_reset_token(user.id)
        # Here you would typically send the reset token to the user's email
        # This is just a placeholder response
        return f"Password reset token generated and sent to {email}", 200

    def verify_token(self, token):
        try:
            user_id = self.auth_service.decode_token(token)
            return True, None
        except Exception as e:  # You might want to catch specific exceptions
            return False, str(e)
