from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.auth_service import AuthService, UserService
import os

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService(secret_key=os.getenv('SECRET_KEY'))
user_service = UserService()

@auth_blueprint.route('/login', methods=['POST'])
def login():
    email, password = request.json.get('email'), request.json.get('password')
    token, error = user_service.authenticate_user(email, password)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"token": token}), 200

@auth_blueprint.route('/register', methods=['POST'])
def register():
    email, password = request.json.get('email'), request.json.get('password')
    user_id, error = user_service.create_user(email, password)
    if error:
        return jsonify({"error": error}), 409
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    message, status = user_service.initiate_password_reset(email)
    return jsonify({"message": message}), status

@auth_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    valid, error = auth_service.verify_token(token)
    if not valid:
        return jsonify({"error": error}), 401
    return jsonify({"message": "Token is valid"}), 200
