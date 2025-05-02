from flask import Flask, request, jsonify
from models.Users import UserModel

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')
userModel = UserModel("data/users.csv")

# @app.route('/')
# def login():
#     return render_template("form.html")

# @app.route('/index_v1', methods=["POST"])
# def index():
#     return render_template("index.html", username=request.form["username"])

@app.route('/users/<int:user_id>')
@app.route('/users')
def get_users(user_id=None):
    return jsonify(userModel.get_users(user_id))

@app.route('/users', methods=["POST"])
def new_user():
    userInput = request.json
    user = userModel.new_user(username=userInput["username"], age=userInput["age"])
    response = jsonify(user)
    response.headers["location"] = f"/users/{user['user_id']}"
    return response

@app.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id=None):
    user = userModel.delete_user(user_id)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=["PUT", "PATCH"])
def update_user(user_id=None):
    username = request.json["username"] if "username" in request.json else None
    age = request.json["age"] if "age" in request.json else None
    user = userModel.update_user(user_id, username=username, age=age)
    return jsonify(user)

if __name__ == '__main__':
    app.run(port=8081)