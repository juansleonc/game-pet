import os
import jwt
from datetime import datetime, timedelta, timezone

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY', '')
        if not self.secret_key:
            raise ValueError("Secret key is not set.")

    def generate_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(user_id)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload['sub'] 
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def verify_token(self, token):
        try:
            print('hello--------------')
            user_id = self.decode_token(token)
            return True, user_id  
        except Exception as e:
            return False, str(e)

    def generate_password_reset_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(hours=2),
            "iat": datetime.now(timezone.utc),
            "sub": str(user_id),
            "scope": "password_reset"
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

