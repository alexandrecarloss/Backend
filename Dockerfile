# Python base
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expondo porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["gunicorn", "raquimic_api.wsgi:application", "--bind", "0.0.0.0:8000"]
