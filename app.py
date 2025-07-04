from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user

app = Flask(__name__, static_url_path='', static_folder='public', template_folder='templates')
app.config.update(SECRET_KEY='my_secret_key')

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    1 : {
        "user_id": 1,
        "username": "test",
        "password": "test",
        "amount": 150000
    },
    2 : {
        "user_id": 2,
        "username": "bad_guy",
        "password": "bad_guy",
        "amount": 0
    }
}

def get_user(id):
    return users.get(id)

@login_manager.user_loader
def user_loader(id):
    user = get_user(int(id))
    if user is not None:
        user_model = UserMixin()
        user_model.id = user["user_id"]
        return user_model
    return None

@app.errorhandler(401)
def unauthorized(error):
    return "Not authorised", 401

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        for user in users.values():
            if username == user["username"] and password == user["password"]:
                user_model = UserMixin()
                user_model.id = user["user_id"]
                login_user(user_model)
                return redirect(url_for("accounts"))
        return abort(401)
    elif current_user.is_authenticated:
        return redirect(url_for('accounts'))
    return render_template("homepage.html")

@app.route("/accounts", methods=['GET', 'POST'])
@login_required
def accounts():
    user = get_user(current_user.id)
    if request.method == 'POST':
        transfer_amount = int(request.form.get("amount"))
        transfer_to = get_user(int(request.form.get("account")))
        if transfer_amount <= user["amount"] and transfer_to is not None:
            user["amount"] -= transfer_amount
            transfer_to["amount"] += transfer_amount
        print("users =>", users)
    return render_template("accounts.html", username=user["username"], amount=user["amount"])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug= True, port=8081)
