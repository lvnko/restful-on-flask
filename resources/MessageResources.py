from flask_restful import Resource, reqparse, request
from flask import after_this_request
from flask import current_app as app

class MessageResources(Resource):
    # Define queue as a class variable
    queue = [] 
    
    def __init__(self):
        # Remove queue initialization from __init__
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("data_date", type=str, help="Data date is required and must be a string.", required=True)
        self.parser.add_argument("location", type=str, help="Location is required and must be a string.", required=True)

    def post(self, user_id):
        
        @after_this_request
        def set_cookie(response):
            response.set_cookie("sent_message_before", value="true")
            response.set_cookie("message_only", value="1", path="/messages")
            return response
        
        app.logger.info(request.cookies)
        token = request.headers.get("token")
        if token is None:
            return None, 401, {"WWW-Authenticate": "Token required"}
        elif not self.is_valid_token(token):
            return None, 403, {"WWW-Authenticate": "Invalid token"}
        else:
            args = self.parser.parse_args()
            # Append to the class variable queue
            MessageResources.queue.append({ 
                "user_id": user_id,
                "data_date": args.get("data_date"),
                "location": args.get("location")
            })
            # Print the class variable queue
            print(MessageResources.queue) 
            return "Acknowledged", 202
    
    def is_valid_token(self, token):
        return token == "xuemi-token"
