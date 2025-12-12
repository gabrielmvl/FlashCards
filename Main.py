from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import Usuario
from Auxiliar import *
from db import db

app = Flask(__name__)
app.secret_key = 'test'
lm = LoginManager(app)
lm.login_view = 'Login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@lm.user_loader
def UserLoader(id):
    try:
        return db.session.query(Usuario).filter_by(id=id).first()
    
    except (ValueError, TypeError):
        return None

@app.route("/")
def home():
    if current_user.is_authenticated:
        UserName = current_user.UserName
        return render_template('home.html', UserName=UserName)
    else:
        return render_template('home.html')

@app.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
      
    if request.method == 'GET':
        return render_template('cadastro.html')
        
    if request.method == 'POST':
        NomeSub = request.form['NomeForm'].lower()
        Nome = F_crypt(NomeSub)
        HashNome = Hash256(NomeSub)
        UserNameSub = request.form['UserNameForm'].lower()
        UserName = F_crypt(UserNameSub)
        HashUserName = Hash256(UserNameSub)
        SenhaSub = request.form['SenhaForm']
        Senha = B_crypt(SenhaSub)
        EmailSub = request.form['EmailForm'].lower()
        Email = F_crypt(EmailSub)
        HashEmail = Hash256(EmailSub)

        ComfirmarSenha = request.form['ComfirmarSenhaForm']

        if not SenhaSub == ComfirmarSenha:
            return render_template('cadastro.html', NomeSub=NomeSub, UserNameSub=UserNameSub, EmailSub=EmailSub)

        else:
            NovoUsuario = DataBase.NovoUsuario(Nome, UserName, Senha, Email, HashNome, HashUserName, HashEmail)
            login_user(NovoUsuario)
            return redirect(url_for("home"))

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        Main = request.form['MainForm'].lower()
        HashMain = Hash256(Main)
        Senha = request.form['SenhaForm']
        RememberLogin = 'RememberLoginForm' in request.form
        user = db.session.query(Usuario).filter_by(HashEmail=HashMain).first()
        if not user:
            user = db.session.query(Usuario).filter_by(HashUserName=HashMain).first()
            if not user:
                return render_template('login.html', NotUser=True, MainSub=Main)
            else:
                Senha_db = user.Senha
                if B_verify(Senha_db, Senha):
                    login_user(user, remember=RememberLogin)
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', NotUser=True, MainSub=Main)
        else:
            Senha_db = user.Senha
            if B_verify(Senha_db, Senha):
                login_user(user, remember=RememberLogin)
                return redirect(url_for('home'))
            else:
                return render_template('login.html', NotUser=True, MainSub=Main)

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
