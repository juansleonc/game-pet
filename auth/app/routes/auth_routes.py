from flask import Blueprint, request, jsonify, current_app as app

from app.models.user import User
from app.services.auth_service import AuthService
from app.services.factories import get_user_service 
from bson import ObjectId
from app.utils import parse_request
from app.handlers import bad_request, unauthorized, conflict, success, created
import os

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_blueprint.route('/login', methods=['POST'])
def login():
    user_service = get_user_service()
    data = parse_request(['email', 'password'])
    token, error = user_service.authenticate_user(data['email'], data['password'])
    if error:
        return unauthorized(error)
    return success({'token': token})

@auth_blueprint.route('/register', methods=['POST'])
def register():
    user_service = get_user_service()
    data = parse_request(['email', 'password'])
    if not data['email'] or not data['password']:
        return bad_request('Email and password are required')

    user_id, error = user_service.create_user(data['email'], data['password'])
    if error:
        return conflict(error)
    return created(f"User created successfully with user_id: {str(user_id)}")


@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    user_service = get_user_service()
    message, status = user_service.initiate_password_reset(email)
    return jsonify({"message": message}), status

@auth_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    if not token:
        return bad_request('Token is required')
    valid, error = auth_service.verify_token(token)
    if not valid:
        return unauthorized(error)
    return success({}, 'Token is valid')
