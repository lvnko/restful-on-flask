from flask import Blueprint
from flask_restful import Api

from .resources.UserResources import UserResources
from .resources.LoginResources import LoginResources
from .resources.LogoutResources import LogoutResources

v2_bp = Blueprint("v2_blueprint", __name__)
api = Api(v2_bp)

api.add_resource(UserResources, "/users", '/users/<int:user_id>')
api.add_resource(LoginResources, "/login")
api.add_resource(LogoutResources, "/logout")