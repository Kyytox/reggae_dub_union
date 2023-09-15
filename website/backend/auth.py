"""
This file contains the code for the authentication of the user.

Registering a new user
Logging in an existing user
Logging out a user
Deleting a user
"""

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from .app import app
from . import db

# from . import app
from .models import User


@app.route("/r")
def register1():
    return "yes"


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user.
    """
    print("register")
    print(request.method)
    print(request.form)
    return "test"
    if request.method == "POST":
        # Get form information.
        name = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists.
        if User.query.filter_by(name=name).first():
            return render_template("error.html", message="User already exists.")

        # Create new user.
        new_user = User(name=name, password=generate_password_hash(password, method="sha256"))

        # Add user to database.
        db.session.add(new_user)
        db.session.commit()

        return render_template("succesAuth.html")

    return render_template("register.html")
