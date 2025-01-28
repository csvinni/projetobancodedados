from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edicao')
def edicao():
    return render_template('edicao.html')

@app.route('/doador', methods = (['GET', 'POST']))
def doador():
    if request.method == 'POST':
        cursor = conexao.connection.cursor()
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        INSERT = 'INSERT INTO doadores(nome,email,telefone) VALUES (%s, %s, %s)'
        
        try:
            cursor.execute(INSERT, (nome, email, telefone)) 
            conexao.connection.commit()  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            cursor.close()

        return render_template('doador.html')

    return render_template('doador.html')

@app.route('/campanhas', methods=['GET', 'POST'])
def campanhas():
    if request.method == 'POST':
        cursor = conexao.connection.cursor()
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        meta_itens = request.form.get('meta_itens')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        INSERT = 'INSERT INTO campanhas(titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim) VALUES (%s, %s, %s, %s, %s, %s)'
        
        try:
            cursor.execute(INSERT, (titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim)) 
            conexao.connection.commit()  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            cursor.close()
        return redirect(url_for('listar_campanhas'))

    return render_template('cadastro_campanhas.html')
    


@app.route('/itens_doacoes',  methods = (['GET', 'POST']))
def itens_doacoes():
    return  render_template('itens_doacoes.html')


@app.route('/listar_campanhas', methods=['GET', 'POST'])
def listar_campanhas():
    cursor = conexao.connection.cursor()
    campanhas = []

    cursor.execute("SELECT * FROM campanhas")
    campanhas = cursor.fetchall() 

    cursor.close()
    return render_template('listar_campanhas.html', campanhas=campanhas)



@app.route('/listar_doadores',  methods = (['GET', 'POST']))
def listar_doadores():
    cursor = conexao.connection.cursor()  
    cursor.execute("SELECT * FROM doadores") 
    doadores = cursor.fetchall() 
    cursor.close()
    return  render_template('listar_doadores.html', doadores=doadores)



@app.route('/relatorios',  methods = (['GET', 'POST']))
def relatorios():
    return  render_template('relatorios.html')


@app.route('/concluida/<int:id>', methods=['POST'])
def concluida(id):
    cursor = conexao.connection.cursor()
    cursor.execute("UPDATE campanhas SET status = 'Concluída' WHERE id = %s", (id,))
    conexao.connection.commit()
    cursor.close()
    return redirect(url_for('listar_campanhas'))



@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    cursor = conexao.connection.cursor()
    cursor.execute('SELECT id, titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim FROM campanhas WHERE id = %s', (id,))
    campanha = cursor.fetchone()
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        meta_itens = request.form.get('meta_itens')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        cursor.execute('UPDATE campanhas SET titulo = %s, descricao = %s, meta_financeira = %s, meta_itens = %s, data_inicio = %s, data_fim = %s WHERE id = %s', 
                       (titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim, id))
        conexao.connection.commit()
        cursor.close()
        
        return redirect(url_for('listar_campanhas'))

    return render_template('editar_campanha.html', campanha=campanha)  # Certifique-se de criar este template