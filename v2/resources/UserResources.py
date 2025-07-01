from flask_restful import Resource, reqparse, fields, marshal_with, request
from ..models.Users import UserModel
from flask import current_app as app
from flask import g, session
import pathlib, os, werkzeug
userModel = UserModel(os.path.join(pathlib.Path(__file__).parent, "../data/users.csv"))

class UserResources(Resource):

    user_fields = {
        "user_id": fields.Integer,
        "username": fields.String,
        "age": fields.Integer
    }
    
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        # Arguments for POST/PUT/PATCH
        self.parser.add_argument("username", type=str, help="Username must be a string.", location=['json', 'form'])
        self.parser.add_argument("age", type=int, help="Age must be an integer.", location=['json', 'form'])
    
    @marshal_with(user_fields)
    def get(self, user_id=None):
        # token = request.headers.get("token")
        # if token is not None and token == "MY_API_SECRET":
        print(f"user_id => {session.get('user_id')}")
        if session.get("user_id") is None:
            raise werkzeug.exceptions.Unauthorized("Please login before accessing this API.")
        print(session)
        # session["user_id"] = 1
        # Parser for GET request query parameters
        get_parser = reqparse.RequestParser(bundle_errors=True)
        get_parser.add_argument("items", type=int, help="It's an integer that represent the number of users.", location='args')
        get_parser.add_argument("offset",  type=int, help="The beginning index of users.", location='args')
        get_parser.add_argument("filter_by", type=str, help="A string to define search criteria.", location='args')
        get_parser.add_argument("sort_by", type=str, help="A string to define sort criteria.", location='args')
        args = get_parser.parse_args()
        # app.logger.info(f"uuid: {g.uuid}, is_connected: {g.conn['is_connected']}")
        return userModel.get_users(
            user_id,
            items=args.get("items"),
            offset=args.get("offset"),
            filter_by=args.get("filter_by"),
            sort_by=args.get("sort_by")
        ), 200 # Corrected: Call on the instance 'userModel'
    
        # else:
        #     return {"message": "Unauthorized access"}, 403

    @marshal_with(user_fields)
    def post(self):
        parser = self.parser
        parser.add_argument("username", type=str, required=True, help="Username is required and must be a string.")
        parser.add_argument("age", type=int, required=True, help="Age is required and must be an integer.")
        args = self.parser.parse_args()
        user = userModel.new_user(username=args["username"], age=args["age"])
        # Corrected return format: (data, status_code, headers)
        return user, 201, {"Location": f"/users/{user['user_id']}"}

    @marshal_with(user_fields)
    def delete(self, user_id):
        user = userModel.delete_user(user_id)
        return user, 200
    
    @marshal_with(user_fields)
    def put(self, user_id):
        return self.update_user(user_id)
    
    @marshal_with(user_fields)
    def patch(self, user_id):
        return self.update_user(user_id)

    def update_user(self, user_id=None):
        args = self.parser.parse_args()
        # Corrected: Use 'args' to get the parsed arguments
        user = userModel.update_user(user_id, username=args.get("username"), age=args.get("age"))
        return user
