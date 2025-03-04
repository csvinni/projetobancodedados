# main.py

from . import banco  # Importa a função banco diretamente
import os

if __name__ == "__main__":
    # Usar o caminho relativo para mysql.sql
    caminho_sql = os.path.join(os.path.dirname(__file__), 'mysql.sql')
    banco(caminho_sql) 
    print("Banco de dados e tabelas inicializados com sucesso!")