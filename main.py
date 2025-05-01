from flask import Flask
from flask import render_template, request
from models.Users import UserModel

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')
userModel = UserModel("data/users.csv")

@app.route('/')
def login():
    return render_template("form.html")

@app.route('/index_v1', methods=["POST"])
def index():
    return render_template("index.html", username=request.form["username"])

@app.route('/users')
def users():
    return render_template("users.html", users=userModel.get_users())

if __name__ == '__main__':
    app.run(port=8081)