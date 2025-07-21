#!/bin/bash

# Script de deploy para o Iara Flow BFF

echo "🚀 Iniciando deploy do Iara Flow BFF..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado. Por favor, configure as variáveis de ambiente."
    echo "📝 Copie o arquivo .env.example e configure as variáveis necessárias:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Corrigir problemas de banco de dados
echo "🔧 Corrigindo configurações de banco de dados..."
python3 fix_database.py

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar os containers
echo "🔨 Construindo e iniciando containers..."
docker-compose up -d --build

# Verificar se o container está rodando
echo "🔍 Verificando status do container..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    echo "✅ Deploy concluído com sucesso!"
    echo "🌐 Aplicação disponível em: http://localhost:5000"
    echo "📊 Para ver os logs: docker-compose logs -f"
    echo "🛑 Para parar: docker-compose down"
else
    echo "❌ Erro no deploy. Verificando logs..."
    docker-compose logs
    exit 1
fi

