from flask import current_app
from .user_service import UserService

def get_user_service():
    service = UserService()
    service.set_mongo(current_app.mongo)
    return service

