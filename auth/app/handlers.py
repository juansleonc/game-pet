from flask import Blueprint
from app.utils import standard_response

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.errorhandler(400)
def bad_request(error):
    return standard_response(400, 'Bad request', {'error': str(error)})

@auth_blueprint.errorhandler(401)
def unauthorized(error):
    return standard_response(401, 'Unauthorized', {'error': str(error)})

@auth_blueprint.errorhandler(409)
def conflict(error):
    return standard_response(409, 'Conflict', {'error': str(error)})

def success(data=None, message='Operation successful'):
    return standard_response(200, message, data)

def created(data=None, message= 'It was created'):
    return standard_response(201, message, data)