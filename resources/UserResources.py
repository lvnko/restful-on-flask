from flask_restful import Resource, reqparse, fields, marshal_with, request
from models.Users import UserModel
from flask import current_app as app
from flask import g
userModel = UserModel("data/users.csv")

class UserResources(Resource):

    user_fields = {
        "user_id": fields.Integer,
        "username": fields.String,
        "age": fields.Integer
    }
    
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("username", type=str, help="Username must be a string.")
        self.parser.add_argument("age", type=int, help="Age must be an integer.")
    
    @marshal_with(user_fields)
    def get(self, user_id=None):
        # 關於原先在這裡被移除的代碼，可以在這個 branch 重溫 : lesson#04
        parser = self.parser
        parser.add_argument("items", type=int, help="It's an integer that represent the number of users.")
        parser.add_argument("offset",  type=int, help="The beginning index of users.")
        parser.add_argument("filter_by", type=str, help="A string to define search criteria.")
        args = parser.parse_args()
        app.logger.info(f"uuid: {g.uuid}, is_connected: {g.conn['is_connected']}")
        return userModel.get_users(
            user_id,
            items=args.get("items"),
            offset=args.get("offset"),
            filter_by=args.get("filter_by")
        ), 200 # Corrected: Call on the instance 'userModel'

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