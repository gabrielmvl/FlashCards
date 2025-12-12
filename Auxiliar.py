import bcrypt
from cryptography.fernet import Fernet
from models import Usuario
from db import db
import hashlib

with open('static/FernetKey.txt', 'rb') as f:
    FernetKey = f.read()
    f = Fernet(FernetKey)

def B_crypt(Item):
    salt = bcrypt.gensalt()
    Item_Criptografado = bcrypt.hashpw(Item.encode(), salt)
    return Item_Criptografado

def B_verify(crypt, digit):
    return bcrypt.checkpw(digit.encode(), crypt)

def F_crypt(Item):
    Item_Criptografado = f.encrypt(Item.encode())
    return Item_Criptografado

def F_decrypt(Item):
    Item_Decriptografado = f.decrypt(Item).decode()
    return Item_Decriptografado
    
def Hash256(Item):
    Item_Criptografado = hashlib.sha256(Item.encode('utf-8')).hexdigest()
    return Item_Criptografado
    
class DataBase:
    def NovoUsuario(Nome, UserName, Senha, Email, HashNome, HashUserName, HashEmail):
        NovoUsuario = Usuario(Nome=Nome, UserName=UserName, Senha=Senha, Email=Email, HashNome=HashNome, HashUserName=HashUserName, HashEmail=HashEmail)
        db.session.add(NovoUsuario)
        db.session.commit()
        return NovoUsuario