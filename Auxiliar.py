import bcrypt
from cryptography.fernet import Fernet

def B_crypt(Item):
    salt = bcrypt.gensalt()
    Item_Criptografado = bcrypt.hashpw(Item.encode(), salt)
    return Item_Criptografado

def F_crypt(Item):
    with open('static/FernetKey.txt', 'rb') as f:
        FernetKey = f.read()
    f = Fernet(FernetKey)
    Item_Criptografado = f.encrypt(Item.encode())
    return Item_Criptografado