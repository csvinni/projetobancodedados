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

@app.route('/doador', methods=['GET', 'POST'])
def doador():
    doador_id = None  # Inicialize a variável doador_id

    # Inicialize o cursor fora do bloco POST
    cursor = None

    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        # Inserindo o doador
        INSERT_D = 'INSERT INTO doadores(nome, email, telefone) VALUES (%s, %s, %s)'
        
        try:
            cursor = conexao.connection.cursor()  # Criação do cursor
            cursor.execute(INSERT_D, (nome, email, telefone)) 
            conexao.connection.commit()  
            doador_id = cursor.lastrowid  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            if cursor:  # Verifique se o cursor foi criado antes de fechá-lo
                cursor.close()

        if doador_id is not None:  # Verifique se doador_id foi definido
            return redirect(url_for('itens_doacao', doador_id=doador_id))
        else:
            return render_template('cadastro_doador.html')  # Mensagem de erro

    # Para lidar com o GET, vamos buscar os doadores
    try:
        cursor = conexao.connection.cursor()  # Criação do cursor para a consulta
        cursor.execute("SELECT id, nome FROM doadores")  # Consulta
        doadores = cursor.fetchall()  # Obtenha os resultados
    except Exception as e:
        print(f"An error occurred while fetching doadores: {e}")
        doadores = []
    finally:
        if cursor:  # Verifique se o cursor foi criado antes de fechá-lo
            cursor.close()

    return render_template('doador.html', doadores=doadores)


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
    


@app.route('/itens_doacao', methods=['POST', 'GET'])
def itens_doacao():
    cursor = conexao.connection.cursor()  
    
    if request.method == 'POST':
        id_doador = request.form.get('id_doador')
        id_campanha = request.form.get('id_campanha')
        tipo_doacao = request.form.get('tipo_doacao')
        
        # Verifique o tipo de doação e obtenha os dados necessários
        if tipo_doacao == 'itens':
            tipo_item = request.form.get('tipo_item')
            quantidade = request.form.get('quantidade')
            valor = None 
        elif tipo_doacao == 'dinheiro':
            tipo_item = None  
            quantidade = None  
            valor = request.form.get('valor')

        data_doacao = request.form.get('data_doacao')

        try:
            # Inserir os dados de doação no banco de dados
            INSERT = '''INSERT INTO doacoes(id_doador, id_campanha, tipo_doacao, tipo_item, quantidade, valor, data_doacao) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)'''

            cursor.execute(INSERT, (id_doador, id_campanha, tipo_doacao, tipo_item, quantidade, valor, data_doacao))
            conexao.connection.commit()
            return redirect(url_for('listar_doacoes'))  
        except Exception as e:
            print(f"An error occurred: {e}")
            conexao.connection.rollback()  
            return "Erro ao registrar doação. Tente novamente mais tarde.", 500  
        finally:
            cursor.close()

 
    try:
        cursor.execute("SELECT id, nome FROM doadores")
        doadores = cursor.fetchall()

        cursor.execute("SELECT id, titulo FROM campanhas")
        campanhas = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM categorias")  
        categorias = cursor.fetchall()

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        doadores = []
        campanhas = []
        categorias = []
    finally:
        cursor.close()

    return render_template('cadastro_itens_doacoes.html', doadores=doadores, campanhas=campanhas, categorias=categorias)

@app.route('/listar_campanhas', methods=['GET', 'POST'])
def listar_campanhas():
    cursor = conexao.connection.cursor()
    campanhas = []

    cursor.execute("SELECT * FROM campanhas")
    campanhas = cursor.fetchall() 

    cursor.close()
    return render_template('listar_campanhas.html', campanhas=campanhas)



@app.route('/listar_doacoes', methods=['GET'])
def listar_doacoes():
    cursor = conexao.connection.cursor()
    cursor.execute("""
        SELECT d.id, do.nome AS doador_nome, c.titulo AS campanha_titulo, 
         d.quantidade, d.valor, d.tipo_doacao, d.data_doacao
        FROM doacoes d
        JOIN doadores do ON d.id_doador = do.id
        JOIN campanhas c ON d.id_campanha = c.id
    """)
    doacoes = cursor.fetchall()
    cursor.close()

    return render_template('listar_doacoes.html', doacoes=doacoes)




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