import os

from flask import Flask, render_template, request, redirect, url_for, session

# App Initialization
from . import create_app  # from __init__ file

app = create_app(os.getenv("CONFIG_MODE"))


@app.route("/")
def index():
    return "Hello World!"


# Applications Routes
from . import auth


if __name__ == "__main__":
    app.run(debug=True)
