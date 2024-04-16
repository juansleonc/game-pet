import jwt
from datetime import datetime, timezone

class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": user_id
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode_token(self, token):
        return jwt.decode(token, self.secret_key, algorithms=["HS256"])
