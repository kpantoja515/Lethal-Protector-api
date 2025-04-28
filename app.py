"""
Lethal Protector-API v0.9.0
(c) 2025 Guajava Inc.
"""
import json
import hashlib
from datetime import datetime
import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask("lethal-protector-api")
CORS(app)

@app.route("/")
def index():
    return set_cors({
        "message": "Welcome to Lethal Protector-API!"
    })

@app.route("/authorize", methods=["POST"])
def authorize():
    payload = request.get_json()
    uname = payload.get("username", "")
    pw = payload.get("password", "")
    full_name = ""
    user_level = -1
    access_token = ""
    message = "Account not found."
    user_level, full_name = authorize_user(uname, pw)
    if 0 <= user_level <= 4:
        access_token = generate_access_token(uname, user_level)
        message = ""
    return set_cors({
        "accessToken": access_token,
        "userLevel": user_level,
        "fullName": full_name,
        "message": message,
    })

@app.route("/get_contents", methods=["GET"])
def get_contents():
    payload = request.args
    uname = payload.get("username", "")
    user_level = payload.get("userLevel", -1)
    access_token = payload.get("accessToken", "")
    try:
        user_level = int(user_level)
    except:
        user_level = -1
    expected_token = generate_access_token(uname, user_level)
    if not (0 <= user_level <= 4) or access_token != expected_token:
        return set_cors({"message": "401: Unauthorized"}), 401
    return set_cors({ "contents": load_contents() })

@app.errorhandler(404)
def page_not_found(e):
    return set_cors({"message": "Page not found."})

##################
# utils #
##################
def authorize_user(uname, pw):
    """ Authenticate user login. """
    # Use actual No/SQL in real projects.
    with open(f"data/mock-account-tbl.json") as file:
        accounts = json.load(file)
    if uname not in accounts:
        return -1, ""
    account = accounts[uname]
    hashed = account["hash"].encode()
    if bcrypt.hashpw(pw.encode(), hashed):
        user_level = account["userLevel"]
        full_name = account["fullName"]
        return user_level, full_name
    return -1, ""

def generate_access_token(uname, user_level):
    """ Create a session token. """
    # Use standard approaches (like JWT) in your future projects.
    today = datetime.now().strftime("%Y-%m")
    message = (uname + str(user_level) + today).encode()
    return hashlib.sha1(message).hexdigest()

def load_contents():
    """ Load all contents. """
    # Use actual No/SQL in real projects.
    with open(f"data/mock-content-tbl.json") as file:
        return json.load(file)

def set_cors(payload):
    """ Wraps payload in a JSON response with CORS headers. """
    response = jsonify(payload)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response 