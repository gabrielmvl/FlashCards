import bcrypt

def B_crypt(Item):
    salt = bcrypt.gensalt()
    Item_Criptografado = bcrypt.hashpw(Item.encode(), salt)
    return Item_Criptografado

def B_verify(crypt, digit):
    return bcrypt.checkpw(digit.encode(), crypt)