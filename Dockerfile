# Usa uma imagem oficial do Python leve
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do projeto
COPY . .

# Expõe a porta que o FastAPI usa
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]