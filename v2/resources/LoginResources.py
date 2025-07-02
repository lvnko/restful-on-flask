from flask_restful import Resource, reqparse
from flask import session
import werkzeug

class LoginResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("username", type=str, help = 'username must be a string.')
        self.parser.add_argument("password", type=str, help = 'password must be a string.')
        self.users = {
            "me": "123"
        }

    def post(self):
        args = self.parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        if self.users.get(username) is not None and self.users.get(username) == password:
            session["user_id"] = 1
            session["is_logged_in"] = True

            for dummy in range(500): # 製造數據量來比較兩種 Sessions 在客戶端所留下的檔案大小差異
                session[f"dummy_{dummy}"] = dummy
        else:
            raise werkzeug.exceptions.BadRequest("username/password cannot be found!")
