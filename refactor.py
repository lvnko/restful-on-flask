from flask import Flask, request, jsonify
from flask_restful import Api
from models.Users import UserModel
from resources.UserResources import UserResources
from resources.ClassResources import ClassResources

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')
api = Api(app)

api.add_resource(UserResources, "/users", '/users/<int:user_id>')
api.add_resource(ClassResources, "/classes", '/classes/<int:class_id>')


if __name__ == '__main__':
    app.run(port=8081)