from flask import Flask
from flask import render_template, request

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def login():
    return render_template("form.html")

@app.route('/index_v1', methods=["POST"])
def index():
    return render_template("index.html", username=request.form["username"])

@app.route('/users')
def users():
    userItems = [
        { "username": "lvnko", "age": 20 },
        { "username": "ivan", "age": 25 },
        { "username": "petko", "age": 30 }
    ]
    return render_template("users.html", users=userItems)

if __name__ == '__main__':
    app.run(port=8081)