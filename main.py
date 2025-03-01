import pymssql
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os

app = FastAPI()

# Configurações de conexão com o SQL Server
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")


@app.get("/vwcliente/")
async def get_vwcliente():
    try:
        # Conectar ao banco de dados usando pymssql
        conn = pymssql.connect(server=SERVER, user=USERNAME,
                               password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Executar a consulta na view vwcliente
        cursor.execute("SELECT top 10 * FROM vwcliente")
        rows = cursor.fetchall()

        # Converter as linhas para uma lista de dicionários
        clientes = [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Retornar a resposta JSON
        return JSONResponse(content=jsonable_encoder(clientes))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {str(e)}")

    finally:
        if conn:
            conn.close()
