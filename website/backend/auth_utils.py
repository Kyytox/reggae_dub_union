"""
Program to store utils functions for authentication
"""

import datetime
import jwt
import os


def encode_auth_token(username):
    """
    Generates a JWT token for the given username.

    Args:
        username (str): The username to generate a token for.

    Returns:
        str: The JWT token.
    """
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1000),
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return token


def decode_auth_token(token):
    """
    Decodes a JWT token and returns the username.

    Args:
        token (str): The JWT token to decode.

    Returns:
        str: The username.
    """
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
