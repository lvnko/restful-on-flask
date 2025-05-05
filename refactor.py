from flask import Flask, request, jsonify, g
from flask_restful import Api
from models.Users import UserModel
from resources.UserResources import UserResources
from resources.ClassResources import ClassResources
from resources.MessageResources import MessageResources
import uuid

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')
api = Api(app)

@app.before_request
def preprocess():
    g.uuid = uuid.uuid4()
    g.conn = { "is_connected": True }

@app.after_request
def postprocess(response):
    g.conn["is_connected"] = False
    app.logger.info(g.conn)
    app.logger.info(response)
    return response

@app.teardown_request
def teardown_process(error):
    app.logger.error(f"user-{g.uuid} has triggered an error: {error}")
    g.conn["is_connected"] = False

api.add_resource(UserResources, "/users", '/users/<int:user_id>')
api.add_resource(ClassResources, "/classes", '/classes/<int:class_id>')
api.add_resource(MessageResources, "/messages/<int:user_id>")


if __name__ == '__main__':
    app.run(port=8081)