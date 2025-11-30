from Auxiliar import B_crypt, B_verify, F_crypt, F_decrypt
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import Usuario
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
        UserName = F_decrypt(current_user.UserName).decode()
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
        UserNameSub = request.form['UserNameForm'].lower()
        SenhaSub = request.form['SenhaForm']
        EmailSub = request.form['EmailForm'].lower()

        Nome = F_crypt(NomeSub)
        UserName = F_crypt(UserNameSub)
        Senha = B_crypt(SenhaSub)
        Email = F_crypt(EmailSub)

        ComfirmarSenha = request.form['ComfirmarSenhaForm']

        if not SenhaSub == ComfirmarSenha:
            return render_template('cadastro.html', NomeSub=NomeSub, UserNameSub=UserNameSub, EmailSub=EmailSub, SenhaSub=SenhaSub, ComfirmarSenhaSub=ComfirmarSenha)

        else:
            NovoUsuario = Usuario(Nome=Nome, UserName=UserName, Senha=Senha, Email=Email)
            db.session.add(NovoUsuario)
            db.session.commit()
            login_user(NovoUsuario)
            return redirect(url_for("home"))

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        Email = request.form['EmailForm'].lower()
        Email_crypt = F_crypt(Email)
        Senha = request.form['SenhaForm']
        user = db.session.query(Usuario).filter_by(Email=Email_crypt).first()
        if not user:
            return render_template('login.html', NotUser=True, EmailSub=Email, SenhaSub=Senha)
        elif user:
            Senha_db = user.Senha
            SenhaIsIncorrect = not B_verify(Senha_db, Senha)
            if SenhaIsIncorrect:
                return render_template('login.html', SenhaIsIncorrect=SenhaIsIncorrect, EmailSub=Email, SenhaSub=Senha)

            else:
                login_user(user)
                return redirect(url_for('home'))

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
