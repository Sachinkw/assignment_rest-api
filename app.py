from flask import Flask, redirect, request, jsonify
from model import db
from config import Config
from controller import post_user, get_data, update_data, delete_data, upload_profile_pic

app = Flask(__name__)

# Setting up all the configurations for app
app.config.from_object(Config)


# All tables get created automaticallly
@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/register/user', methods=["POST"])
def register():
    if request.method=="POST":
        return post_user(request.json)


@app.route('/get/user/<email>', methods=["GET"])
def get_user(email):
    if request.method=="GET":
        return get_data(email)


# As this endpoint is able to update the partial data, so we are using PATCH method
@app.route('/update/user', methods=["PATCH"])
def user_update():
    if request.method=="PATCH":
        return update_data(request.json)


@app.route('/upload/pic', methods=["POST", "PUT"])
def upload_pic():
    if request.method in ["POST", "PUT"]:
        if 'photo' in request.files:
            # pass photo file and user_id in the argument
            return upload_profile_pic(request.files, request.args)
        # return redirect(request.url)
        else:
            return jsonify({"message":"No image"})


@app.route('/delete/user', methods=["DELETE"])
def delete_user():
    if request.method=="DELETE":
        return delete_data(request.args)


if __name__=="__main__":
    db.init_app(app)
    app.run(debug=True)

