from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer(), primary_key=True)

    UserName = db.Column(db.String(30), unique=True)

    Nome = db.Column(db.String())

    Senha = db.Column(db.String())

    Email = db.Column(db.String(), unique=True)