#Flask é o microframework que será utilizado
from flask import Flask, render_template, request
# SQLite é o banco de dados embutido que será utilizado
import sqlite3
# Bibliotecas utilizadas para lidar com valores do tipo data
import time
from datetime import date

# Conecta ao banco de dados local usando a variável db
db = sqlite3.connect("data/database.db", check_same_thread=False)
# __name__ é apenas uma maneira conveniente de obter o nome de importação do local em que o aplicativo está definido. O frasco usa o
#import name para saber onde procurar recursos, templates, static files, instance folder, etc.
app = Flask(__name__, template_folder='templates')
#app.route("/") define o valor da url, para o valor ("/") podemos usar de exemplo site.com/
@app.route("/")
def index():
#A função index retorna o valor render_template(), que renderiza alguma página html no navegador
    return render_template("index.html")

@app.route("/novo_projeto")
def novo_projeto():
    return render_template("novo_projeto.html")

@app.route("/novo_projeto", methods=["POST"])
def cria_novo_projeto():
# request.form.get(), atribui a variável um valor com base em um formulário html, aonde o valor dentro do parenteses
# refere-se a tag html input, para a primeira variável dessa função, a que tem name = nome_do_projeto
    nome_do_projeto = request.form.get("nome_do_projeto")
    data_de_inicio = request.form.get("data_de_inicio")
    data_de_fim = request.form.get("data_de_fim")
# db.execute() faz com que seja executado a query SQL dentro do banco refernciado na variável db
    db.execute("INSERT INTO tabela_projetos(nome_do_projeto, data_de_inicio, data_de_fim) VALUES (?,?,?)", (nome_do_projeto, data_de_inicio, data_de_fim))
# db.commit() salva as alterações feita ao banco de dados na vriável db
    db.commit()
    return render_template("novo_projeto.html")

@app.route("/nova_atividade")
def nova_atividade():
    lista_de_projetos = db.execute("SELECT id, nome_do_projeto FROM tabela_projetos").fetchall()
    return render_template("nova_atividade.html", projetos=lista_de_projetos)

@app.route("/nova_atividade", methods=["GET","POST"])
def cria_nova_atividade():
    id_atividade = request.form.get("id_atividade")
    id_do_projeto = request.form.get("id_do_projeto")
    nome_da_atividade = request.form.get("nome_da_atividade")
    data_de_inicio = request.form.get("data_de_inicio")
    data_de_fim = request.form.get("data_de_fim")
    finalizada = request.form.get("finalizada")

    db.execute("INSERT INTO tabela_atividades(id_atividade, id_do_projeto, nome_da_atividade, data_de_inicio, data_de_fim, finalizada) VALUES (?,?,?,?,?,?)", (id_atividade, id_do_projeto, nome_da_atividade, data_de_inicio, data_de_fim, finalizada))
    db.commit()

    return nova_atividade()
@app.route("/projetos")
def lista_de_projetos():
    lista_de_projetos = db.execute("SELECT id, nome_do_projeto FROM tabela_projetos").fetchall()
    return render_template("projeto.html", lista_de_projetos=lista_de_projetos)

@app.route("/projeto", methods=["POST"])
def detalhes_do_projeto():
    id_do_projeto = request.form.get("id_do_projeto")

    projeto = db.execute("SELECT id, nome_do_projeto, data_de_inicio, data_de_fim FROM tabela_projetos WHERE id = ?", (id_do_projeto)).fetchone()
    lista_de_atividades = db.execute("SELECT id_atividade, nome_da_atividade, data_de_inicio, data_de_fim, finalizada FROM tabela_atividades WHERE id_do_projeto = ? ORDER BY data_de_inicio ASC", (id_do_projeto)).fetchall()

    data_fim_projeto = time.strptime(projeto[3], "%Y-%m-%d")
# Para conseguir a data atual precisamos usar essas duas bibliotecas, time e datetime, primeiro usando a função date de
# datatime iremos requisitar a data de hoje, após isso usado o método .strftime() transformaremos esse valor em uma string
# então com o método .strptime() transformamos a string em um objeto datetime
    data_de_hoje = date.today()
    data_de_hoje = data_de_hoje.strftime("%Y-%m-%d")
    data_de_hoje = time.strptime(data_de_hoje, "%Y-%m-%d")

    atrasado = False

    try: incompletas
    except NameError: incompletas = 0

    for atividade in lista_de_atividades:
        data_fim_atividade = time.strptime(atividade[3], "%Y-%m-%d")

        if (atividade[4] == "False"):
            incompletas += 1

        if (data_de_hoje > data_fim_projeto or data_fim_atividade > data_fim_projeto):
            atrasado = True

    porcentagem_completa = 100 - (incompletas * 100 / len(lista_de_atividades))

    return render_template("detalhes.html", projeto=projeto, lista_de_atividades=lista_de_atividades, atrasado=atrasado, porcentagem_completa=porcentagem_completa)
