from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    Username = db.Column(db.String(30), unique=True)

    Senha = db.Column(db.String())

    Email = db.Column(db.String(), unique=True)