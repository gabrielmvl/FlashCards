from db import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer(), primary_key=True)

    UserName = db.Column(db.String(), unique=True)

    HashUserName = db.Column(db.String(), unique=True)

    Nome = db.Column(db.String())

    HashNome = db.Column(db.String())

    Senha = db.Column(db.String())

    Email = db.Column(db.String(), unique=True)

    HashEmail = db.Column(db.String(), unique=True)