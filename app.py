import os
import pyodbc
from flask import Flask, jsonify
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Variáveis de ambiente para a conexão com o banco de dados
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Função para conectar ao banco de dados SQL Server


def get_db_connection():
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DB_SERVER},{DB_PORT};'
        f'DATABASE={DB_NAME};'
        f'UID={DB_USER};'
        f'PWD={DB_PASSWORD}'
    )

    conn = pyodbc.connect(connection_string)
    return conn

# Rota para obter os dados da tabela vwcliente


@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 * FROM vwcliente")
        rows = cursor.fetchall()

        # Organize os dados em um formato de dicionário
        clientes = []
        for row in rows:
            # ajuste conforme as colunas
            cliente = {'id': row[0], 'nome': row[1], 'email': row[2]}
            clientes.append(cliente)

        cursor.close()
        conn.close()

        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
