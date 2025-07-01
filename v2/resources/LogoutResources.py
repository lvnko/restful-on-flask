from flask_restful import Resource
from flask import session

class LogoutResources(Resource):
    def __init__(self):
        pass

    def post(self):
        # session.pop("user_id", default=None)
        # session.pop("is_logged_in", default=None)
        session.clear()