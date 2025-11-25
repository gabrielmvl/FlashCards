from Auxiliar import B_crypt
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import Usuario
from db import db

app = Flask(__name__)
app.secret_key = 'test'
lm = LoginManager(app)
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
  return render_template('home.html')

@app.route("/Cadastro", methods=['GET', 'POST'])
def Cadastro():

  if current_user.is_authenticated:
    return redirect(url_for("home"))
      
  if request.method == 'GET':
    return render_template('cadastro.html')
        
  if request.method == 'POST':
    Nome = request.form['NomeForm'].lower()
    UserName = request.form['UserNameForm'].lower()
    Senha = B_crypt(request.form['SenhaForm'])
    Email = request.form['EmailForm'].lower()

    NovoUsuario = Usuario(Nome=Nome, UserName=UserName, Senha=Senha, Email=Email)

    db.session.add(NovoUsuario)
    db.session.commit()

    login_user(NovoUsuario)

    return redirect(url_for("home"))

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   
  if current_user.is_authenticated:
     return redirect(url_for('home'))

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
            db.create_all()
    app.run()