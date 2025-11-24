#import uuid, bcrypt
from Auxiliar import GerarId
from flask import Flask, render_template, request, redirect, url_for
from models import Usuario
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@app.route("/")

def home():
  return render_template('home.html')

@app.route("/Cadastro", methods=['GET', 'POST'])

def Cadastro():
      
  if request.method == 'GET':
    return render_template('cadastro.html')
        
  if request.method == 'POST':
    Nome = request.form['NomeForm']
    UserName = request.form['UserNameForm']
    Senha = request.form['SenhaForm']
    Email = request.form['EmailForm']

    NovoUsuario = Usuario(Nome=Nome, UserName=UserName, Senha=Senha, Email=Email)

    db.session.add(NovoUsuario)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
            db.create_all()
    app.run(debug=True)