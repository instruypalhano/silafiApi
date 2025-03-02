from fastapi import FastAPI, HTTPException
import pyodbc
from dotenv import load_dotenv
import os

app = FastAPI()

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de conexão com o SQL Server
conn_str = (
    f"DRIVER={os.getenv('DB_DRIVER')};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')}"
)


@app.on_event("startup")
def startup():
    global conn
    conn = pyodbc.connect(conn_str)


@app.on_event("shutdown")
def shutdown():
    conn.close()


@app.get("/dados")
def get_dados():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 100 * FROM vwcliente')
        rows = cursor.fetchall()

        # Obter os nomes das colunas
        columns = [column[0] for column in cursor.description]

        # Transformar os dados em um formato adequado para JSON
        dados = [dict(zip(columns, row)) for row in rows]

        return dados
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {e}")
