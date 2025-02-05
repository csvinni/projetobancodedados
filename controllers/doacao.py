

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

