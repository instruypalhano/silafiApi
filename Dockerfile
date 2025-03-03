# Use uma imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos do projeto para dentro do container
COPY . /app

# Instale as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Defina a variável de ambiente para não rodar o Flask em modo de debug
ENV FLASK_ENV=production

# Exponha a porta onde a aplicação Flask estará rodando
EXPOSE 5000

# Defina o comando para rodar a aplicação
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
