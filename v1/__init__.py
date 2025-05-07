from flask import Blueprint
from flask_restful import Api

from .resources.UserResources import UserResources
from .resources.ClassResources import ClassResources
from .resources.MessageResources import MessageResources

v1_bp = Blueprint("v1_blueprint", __name__)
api = Api(v1_bp)

api.add_resource(UserResources, "/users", '/users/<int:user_id>')
api.add_resource(ClassResources, "/classes", '/classes/<int:class_id>')
api.add_resource(MessageResources, "/messages/<int:user_id>")