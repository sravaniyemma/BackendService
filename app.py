import requests
from flask import Flask, Response, redirect, url_for, request, render_template, json, \
    make_response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, \
    login_required, logout_user

app = Flask(__name__)


app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)
CORS(app)
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login_user():
    username = request.form['username']
    password = request.form['password']
    return render_template('login.html')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    return redirect(url_for("display_posts"))


@app.route('/GetAllUsers', methods=['GET'])
def get_users():
    getAllUsersApi = "https://peter-htet.outsystemscloud.com/ITDInterviews/rest/Users/GetAllUsers"
    r = requests.get(getAllUsersApi)
    data = r.json()
    print(data)
    jsonStr = json.dumps(data)

    return make_response(jsonStr)


@app.route('/GetUser/<name>', methods=['GET'])
def create_product(name):
    getUserApi = "https://peter-htet.outsystemscloud.com/ITDInterviews/rest/Users/GetUser?name="
    r = requests.get(getUserApi, params=name)
    data = r.json()
    jsonStr = json.dumps(data)
    print(data)
    return make_response(jsonStr, 200)


@app.route('/DeleteUser/<id>', methods = ['DELETE'])
def delete_product_by_id(id: any):
    deleteUserApi = "https://peter-htet.outsystemscloud.com/ITDInterviews/rest/Users/DeleteUser?id=";
    response = requests.delete(deleteUserApi, params={id: id})

    return make_response("",204)


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(port=5001)
