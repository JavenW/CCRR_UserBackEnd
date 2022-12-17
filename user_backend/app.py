
from flask import Flask, Response, request, redirect, url_for
from datetime import datetime
import json
from user_database import UserResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.route("/users", methods=["GET"])
def get_all_users():
    result = UserResource.get_users()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/users/<email>", methods=["GET"])
def get_allergy(email):
    result = UserResource.get_user_by_email(email)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


#@app.route("/login", methods=["POST"])
def add_user(email, name, allergy):
    #email = request.args.get('email')
    #name = request.args.get('name')
    #allergy = request.args.get('allergy')
    #print(email, name, allergy)
    UserResource.add_user_by_info(email, name, allergy)


#@app.route("/l", methods=["DELETE"])
def delete_user(email):
    #email = request.args.get('email')
    UserResource.delete_user_by_email(email)


def delete_allergy(email, allergy):
    UserResource.delete_allergy_by_email_and_allergy(email, allergy)


#@app.route("/login", methods=["POST"])
def update_phone(email, phone):
    UserResource.update_phone_by_email_and_phone(email, phone)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5011)


