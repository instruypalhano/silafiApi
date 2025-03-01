from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pyodbc
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Configurações de conexão com o SQL Server (lidas do .env)
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DRIVER = os.getenv("DB_DRIVER")

# String de conexão
CONNECTION_STRING = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'


@app.get("/vwcliente/")
async def get_vwcliente():
    conn = None
    try:
        # Conectar ao banco de dados
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Executar a consulta na view vwcliente
        cursor.execute("SELECT top 10 * FROM vwcliente")
        rows = cursor.fetchall()

        # Converter as linhas para uma lista de dicionários
        clientes = [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Usar jsonable_encoder para serializar os dados
        clientes_serializados = jsonable_encoder(clientes)

        # Retornar a resposta JSON
        return JSONResponse(content=clientes_serializados)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {str(e)}")

    finally:
        if conn:
            conn.close()
