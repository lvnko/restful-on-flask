from flask_restful import Resource, fields, marshal_with
from .UserResources import UserResources, userModel

class ClassSizeField(fields.Raw):
    def format(self, users):
        return len(users)

class ClassResources(Resource):

    class_fields = {
        "class_id": fields.Integer(default=-1),
        "class_name": fields.String(default=""),
        "class_size": ClassSizeField(attribute="users"),
        "users": fields.List(fields.Nested(UserResources.user_fields), default=[])
    }

    def __init__(self):
        self.classes = {
            0: {
                "class_id": 0,
                "class_name": "Math",
                "users": [0,1,3,5,6,11]
            },
            1: {
                "class_id": 1,
                "class_name": "English",
                "users": [5,6,7,9,13]
            },
            2: {
                "class_id": 2,
                "class_name": "History",
                "users": [0, 2, 4, 8, 10]
            },
            3: {
                "class_id": 3,
                "class_name": "Science",
                "users": [1, 3, 7, 11, 12]
            },
            4: {
                "class_id": 4,
                "class_name": "Art",
                "users": [2, 4, 6, 8, 10, 13]
            }
        }
    
    @marshal_with(class_fields)
    def get(self, class_id=None):
        if class_id is None:
            return [self.pack_users_into_their_class(class_copy) for class_copy in self.classes.values()]
        elif class_id in self.classes:
            return self.pack_users_into_their_class(self.classes[class_id])
        else:
            return {}
    
    def pack_users_into_their_class(self, class_input):
        class_copy = class_input.copy()
        class_copy["users"] = list(map(self.get_user_by_user_id, class_copy["users"]))
        return class_copy

    def get_user_by_user_id(self, user_id):
        return userModel.get_users(user_id)
