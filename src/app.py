#from crypt import methods
#from importlib.metadata import requires
from datetime import datetime
#from types import CellType
from flask import Flask, render_template,request, url_for, redirect, session
from flask_mysqldb import MySQL
import funcs

app = Flask(__name__)
app.secret_key = 'super secret key'
# Conexão ao banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306 #Caso a porta seja a padrão, comentar linha.
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mcs2809'
app.config['MYSQL_DB'] = 'pynk'

mysql = MySQL(app)
# Bloco de Paginas.

# Resumo dos comandos 
    #Route  -> Caminho das paginas.
    #Def    -> Função de exibição da pagina.

#Pagina inicial
@app.route("/")
def index():
    return render_template('login.html')
#------------------------------

@app.route("/home", methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

#Pagina de login
@app.route("/cadastroold.html", methods = ['POST', 'GET'])
def cadastro():
    if request.method == "POST":
        #Variaveis vindas do FORM vindas do cadastro.html
        nome            = request.form['name']
        cpf             = request.form['cpf']
        endereco        = request.form['endereco']
        datanascimento  = request.form['datanasc']
        genero          = request.form['genero']
        senha           = request.form['senha']
        login           = request.form['login']
        tipoconta       = request.form['tipoconta']
        funcs.InsMySQL('tb_usuario',CampoBd=['cpf', 'nome', 'genero', 'endereco', 'senha','login', 'datanascimento'],
                       CampoFm=[cpf,nome,genero,endereco, senha, login,datanascimento])
        
        id_usuario = funcs.SlcEspecificoMySQL('tb_usuario', CampoBd=['cpf'], CampoFm=[cpf], CampoEs=['id_usuario'])
        
        funcs.InsMySQL('tb_contabancaria', CampoBd=['id_usuario', 'id_agencia', 'tipo', 'data_abertura', 'saldo'],
                        CampoFm=[id_usuario[0], 1, tipoconta, datetime.today(), 0])

    return render_template('cadastroold.html')
#------------------------------

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        login         = request.form['login']
        senha       = request.form['senha']
        resultado   = funcs.SlcMySQL('tb_usuario',CampoBd=['login','senha'],CampoFm=[login,senha])
    if resultado:
        session['login']    = True
        session['nome']     = resultado[1]
        return home()
    else:
        return index()

#Bloco para subir o site.
if __name__ == "__main__":
    app.run(debug=True)
   
