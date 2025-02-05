
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
        status = request.form.get('status')

        INSERT = 'INSERT INTO campanhas(titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim,status) VALUES (%s, %s, %s, %s, %s, %s,%s)'
        
        try:
            cursor.execute(INSERT, (titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim, status)) 
            conexao.connection.commit()  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            cursor.close()
        return redirect(url_for('listar_campanhas'))

    return render_template('cadastro_campanhas.html')
    

@app.route('/listar_campanhas', methods=['GET', 'POST'])
def listar_campanhas():
    cursor = conexao.connection.cursor()
    query = "SELECT * FROM campanhas"
    params = []
    
    datainicial_filter = request.args.get('data-inicial')
    datafinal_filter = request.args.get('data-final')

    if datafinal_filter and datainicial_filter:
        query += " WHERE data_inicio >= %s and data_fim <= %s"
        params.append(datainicial_filter)
        params.append(datafinal_filter)
    else:
        if datainicial_filter:
            query += " WHERE data_inicio >= %s"
            params.append(datainicial_filter)
        if datafinal_filter:
            query += " WHERE data_fim <= %s"
            params.append(datafinal_filter)
    # if prioridade_filter:
    #     query += " AND prioridade = %s"
    #     params.append(prioridade_filter)
    # if categoria_filter:
    #     query += " AND categoria = %s"
    #     params.append(categoria_filter)

    cursor.execute(query, params)
    campanhas = cursor.fetchall()

    cursor.close()
    return render_template('listar_campanhas.html', campanhas=campanhas)



@app.route('/relatorios',  methods = (['GET', 'POST']))
def relatorios():

    cursor = conexao.connection.cursor()
    query = "SELECT SUM(valor) FROM doacoes"
    params = []
    
    datainicial_filter = request.args.get('data-inicial')
    datafinal_filter = request.args.get('data-final')

    if datafinal_filter and datainicial_filter:
        query += " WHERE data_doacao >= %s and data_doacao <= %s"
        params.append(datainicial_filter)
        params.append(datafinal_filter)
    else:
        if datainicial_filter:
            query += " WHERE data_doacao >= %s"
            params.append(datainicial_filter)
        if datafinal_filter:
            query += " WHERE data_doacao <= %s"
            params.append(datafinal_filter)
  
    cursor.execute(query, params)
    totalarrecadado = cursor.fetchone()
    total = totalarrecadado['SUM(valor)']

    query_top_donors = """
        SELECT d.nome, SUM(do.valor) AS total_doacao
        FROM doacoes do
        JOIN doadores d ON d.id = do.id_doador
        GROUP BY d.nome
        ORDER BY total_doacao DESC
        LIMIT 10
    """

    cursor.execute(query_top_donors)
    top_donors = cursor.fetchall()  # Lista dos maiores doadores

    cursor.close()

    return render_template('relatorios.html', total=total, top_donors=top_donors)


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
    cursor.execute('SELECT id, titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim, status FROM campanhas WHERE id = %s', (id,))
    campanha = cursor.fetchone()
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        meta_itens = request.form.get('meta_itens')
        data_inicio = request.form.get('data_inicio')
        status = request.form.get('status')
        data_fim = request.form.get('data_fim')

        cursor.execute('UPDATE campanhas SET titulo = %s, descricao = %s, meta_financeira = %s, meta_itens = %s, data_inicio = %s, data_fim = %s, status = %s WHERE id = %s', 
                       (titulo, descricao, meta_financeira, meta_itens, data_inicio, data_fim, status, id))
        conexao.connection.commit()
        cursor.close()
        
        return redirect(url_for('listar_campanhas'))

    return render_template('editar_campanha.html', campanha=campanha)  # Certifique-se de criar este template