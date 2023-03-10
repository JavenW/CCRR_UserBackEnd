from flask import Flask, Response, request, redirect, url_for
import json
from flask_cors import CORS
import os
from oauthlib.oauth2 import WebApplicationClient
import requests
from user import User


# Configuration
GOOGLE_CLIENT_ID = "xxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "xxxxx"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# Create the Flask application object.
application = Flask(__name__)
application.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@application.route("/getallergy", methods=["GET"])
def get_allergy():
    userid = request.args.get('userid', None)
    token = request.args.get('token', None)
    print(userid)
    print(token)
    res = User.checkAuthToken(userid, token)
    if not res:
        return Response(json.dumps({}), status=403, content_type="app.json")
    result = User.get_user_allergy_by_id(userid)
    if result or result == []:
        rsp = Response(json.dumps(result), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@application.route("/addallergy", methods=["POST"])
def add_allergy():
    userid = request.args.get('userid', None)
    token = request.args.get('token', None)
    res = User.checkAuthToken(userid, token)
    if not res:
        return Response(json.dumps({}), status=403, content_type="app.json")
    allergy = request.args.get('allergy', None)
    User.add_allergy_by_user_id(userid, allergy)
    return Response(json.dumps({}), status=200, content_type="app.json")


@application.route("/deleteallergy", methods=["POST"])
def delete_allergy():
    userid = request.args.get('userid', None)
    token = request.args.get('token', None)
    res = User.checkAuthToken(userid, token)
    if not res:
        return Response(json.dumps({}), status=403, content_type="app.json")
    allergy = request.args.get('allergy', None)
    User.delete_allergy_by_user_id(userid, allergy)
    return Response(json.dumps({}), status=200, content_type="app.json")


@application.route("/checklogin", methods=["GET"])
def checklogin():
    print("here1")
    # id = request.form['userid']
    id = request.args.get('userid', None)
    print("here2")
    # token = request.form['authtoken']
    token = request.args.get('authtoken', None)
    print("here3")
    res = User.checkAuthToken(id, token)
    if res:
        return Response(json.dumps({}), status=200, content_type="app.json")
    else:
        return Response(json.dumps({}), status=403, content_type="app.json")

@application.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    # return redirect(request_uri)
    response = redirect(request_uri)
    response.headers = {"Access-Control-Allow-Origin": "*",
        'Access-Control-Allow-Headers': "*",
        'Access-Control-Allow-Methods': "*"}
    return response


@application.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    auth_token = User.encode_auth_token(unique_id, application.config.get('SECRET_KEY'))

    # Doesn't exist? Add to database
    if not User.checkUser(unique_id):
        User.create(unique_id, users_name, users_email, picture, auth_token)
    else:
        # Begin user session by logging the user in
        User.update_authtoken(unique_id, auth_token)

    # Send user back to homepage
    return redirect("http://localhost:3000/loginComplete?userid="+unique_id+"&name="+users_name+"&email="+users_email+"&pict="+picture+"&authtoken="+auth_token)



@application.route("/logout")
def logout():
    userid = request.form['userid']
    User.logout(userid)
    return Response(json.dumps({}), status=200, content_type="app.json")



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
    # app.run(ssl_context="adhoc")
    application.run(host="0.0.0.0", port=8000)


