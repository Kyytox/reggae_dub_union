from app import app


@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Get a list of users.
    """
    # This is a placeholder for the actual implementation.
    # In a real application, you would fetch users from a database.
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]

    return {"users": users}, 200
