import bcrypt
import uuid
import csv
import getpass
import os
from cryptography.fernet import Fernet
import time


Dados = {}
FernetKey = open('Outros/FlashCards/FernetKey.txt', 'rb').read()
f = Fernet(FernetKey)

def Limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def gerarSalt():
    salt = bcrypt.gensalt()
    return salt

def gerar_id():
    id = str(uuid.uuid4())
    return id

def BancoDeDados():

    with open('Usuarios.csv', 'r', encoding='utf-8') as f:
        BancoDeDados = csv.reader(f, delimiter=';')
        for usuario in BancoDeDados:
            Email = usuario[0]
            UserName = usuario[1]
            Senha = usuario[2]
            Id = usuario[3]
            Dados[Email] = [UserName, Senha, Id]

def ColetarDados(metodo):
    Email = input("Digite seu e-mail: ")
    Limpar()

    if metodo == "registro":
        UserName = input("Digite seu username: ")
    Limpar()
    while True:
        Senha = getpass.getpass("Digite sua senha: ")
        Limpar()
        if metodo == "registro":
            ConfirmarSenha = getpass.getpass("Confirme sua senha: ")
            Limpar()

        if Senha != ConfirmarSenha:
            print("Senhas não coencidem")
            time.sleep(2)

        else: break

    if metodo == "registro":
        return UserName, Email, Senha

    else:
        return Email, Senha

def registro():
    UserName, Email, Senha = ColetarDados('registro')
    Salt = gerarSalt()
    id = gerar_id()
    Crypt_UserName = f.encrypt(UserName.encode())
    Crypt_Email = f.encrypt(Email.encode())
    Crypt_Senha = bcrypt.hashpw(Senha.encode(), Salt)
    with open('Usuarios.csv', 'a', encoding='utf-8') as file:
        csv.writer(file, delimiter=';').writerow([Crypt_Email.decode(), Crypt_UserName.decode(), Crypt_Senha.decode(), id])

def Menu():
    while True:
        Menu = input("""Bem vindo ao menu:

        1 - Registrar-se
        2 - Login
        3 - Esqueci a senha

        Qual Opção deseja: """)

        match Menu:
            case '1':
                Limpar()
                registro()
                Limpar()
                return

if __name__ == "__main__":
    Limpar()
    Menu()
    Limpar()