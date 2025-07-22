FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para banco de dados com permissões corretas
RUN mkdir -p /app/data && chmod 755 /app/data

# Expor porta
EXPOSE 5000

# Definir variáveis de ambiente
ENV FLASK_ENV=production
ENV DB_PATH=/app/data/iara_flow.db
ENV HOST=0.0.0.0
ENV PORT=5000

# Comando para executar a aplicação
CMD ["python", "app/main.py"]

