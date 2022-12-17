
from flask import Flask, Response, request, redirect, url_for
from datetime import datetime
import json
from user_database import UserResource
from flask_cors import CORS
import boto3

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


# @app.route("/users", methods=["GET"])
# def get_all_users():
#     result = UserResource.get_users()
#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="app.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")
#     return rsp

@app.route("/getallergy/<email>", methods=["GET"])
def get_allergy(email):
    result = UserResource.get_user_allergy_by_email(email)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/addallergy", methods=["post"])
def add_allergy():
    email = request.form['email']
    allergy = request.form['allergy']
    UserResource.add_allergy_by_email(email, allergy)

    return Response(json.dumps({}), status=200, content_type="app.json")

@app.route("/deleteallergy", methods=["post"])
def delete_allergy():
    email = request.form['email']
    allergy = request.form['allergy']
    UserResource.delete_allergy_by_email(email, allergy)

    return Response(json.dumps({}), status=200, content_type="app.json")


@app.route("/login", methods=["POST"])
def add_user():
    email = request.form['email']
    name  = request.form['name']

    client = boto3.client('ses')
    res = client.list_identities(
        IdentityType='EmailAddress'
    )
    identities = res['Identities']
    if email not in identities:
        client.verify_email_identity(
            EmailAddress=email
        )
    
    user_id = UserResource.get_userid_by_email(email)
    if user_id == -1:
        UserResource.add_user_by_info(email, name)


    return Response(json.dumps({}), status=200, content_type="app.json")


#@app.route("/l", methods=["DELETE"])
# def delete_user(email):
    #email = request.args.get('email')
    # UserResource.delete_user_by_email(email)


#@app.route("/login", methods=["POST"])
# def update_phone(email, phone):
#     UserResource.update_phone_by_email_and_phone(email, phone)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5011)


