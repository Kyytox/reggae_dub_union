"""
This file contains the code for the authentication of the user.

Signup a new user
Logging in an existing user
Logging out a user
Deleting a user
"""

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app

# Utils
from routes.auth_utils import encode_auth_token, decode_auth_token
from models.models import User


@app.route("/api/signup", methods=["POST"])
def Signup():
    """
    Signup a new user.
    """
    print("-------------------------------------------")
    body = request.get_json()["body"]
    print(f"Received body: {body}")

    # Get form information.
    name = body["username"]
    email = body["email"]
    password = body["password"]

    name_not_auth = ["null", "undefined", "None", "nan", "NaN", ""]

    # Check if user already exists.
    if User.query.filter_by(user_name=name).first() or name in name_not_auth:
        return "User already exists"

    # Create new user.
    new_user = User(
        user_name=name,
        user_email=email,
        user_password=generate_password_hash(password),
    )

    # Add user to database.
    new_user.save()

    # generate token
    token = encode_auth_token(name)

    return {"id": new_user.user_id, "user": name, "isAuth": True, "token": token}


@app.route("/api/login", methods=["POST"])
def Login():
    """
    Logging in an existing user.
    """
    body = request.get_json()["body"]
    print(f"Received body: {body}")

    # Get form information.
    name = body["username"]
    # emil = body["email"]
    password = body["password"]

    # Check if user exists.
    user = User.query.filter_by(user_name=name).first()

    # Check if password is correct.
    if not user:
        return "User does not exist"
    if not check_password_hash(user.user_password, password):
        return "Password is incorrect"
    print(user.user_id)

    # generate token
    token = encode_auth_token(name)

    return {"id": user.user_id, "user": name, "isAuth": True, "token": token}
