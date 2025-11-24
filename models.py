from db import db
import uuid
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

    UserName = db.Column(db.String(30), unique=True)

    Nome = db.Column(db.String())

    Senha = db.Column(db.String())

    Email = db.Column(db.String(), unique=True)