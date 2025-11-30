import bcrypt
from cryptography.fernet import Fernet

def B_crypt(Item):
    salt = bcrypt.gensalt()
    Item_Criptografado = bcrypt.hashpw(Item.encode(), salt)
    return Item_Criptografado

def B_verify(crypt, digit):
    return bcrypt.checkpw(digit.encode(), crypt)

def GetFernetKey():
    with open('static/FernetKey.txt', 'rb') as f:
        Key = f.read()
        return Key

FernetKey = GetFernetKey()
f = Fernet(FernetKey)

def F_crypt(Item):
    Item_Criptografado = f.encrypt(Item.encode())
    return Item_Criptografado

def F_decrypt(Item):
    Item_Decriptografado = f.decrypt(Item)
    return Item_Decriptografado