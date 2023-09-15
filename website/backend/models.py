from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # def __init__(self, name, password):
    #     self.name = name
    #     self.password = password

    # def __repr__(self):
    #     return f"<User {self.name}>"

    # def serialize(self):
    #     return {"id": self.id, "name": self.name, "password": self.password}

    # def serialize_no_password(self):
    #     return {"id": self.id, "name": self.name}
