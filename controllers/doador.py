
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

    return render_template('listar_doadores.html', doadores=doadores)

