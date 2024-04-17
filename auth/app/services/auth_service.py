import jwt
from datetime import datetime, timedelta, timezone

class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(user_id)  # Asegurando que el user_id sea una cadena si no lo es
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256").decode('utf-8')  # Asegura compatibilidad entre Python 2 y 3

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload['sub'], None  # Retorna el user_id y ningún error
        except jwt.ExpiredSignatureError:
            return None, "Token has expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"

    def generate_password_reset_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(hours=2),  # Tiempo más corto para reseteo de contraseña
            "iat": datetime.now(timezone.utc),
            "sub": str(user_id),
            "scope": "password_reset"  # Indicar el propósito del token
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256").decode('utf-8')

