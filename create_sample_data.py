#!/usr/bin/env python3
"""
Script para criar dados padrão no banco de dados iara-flow-bff
"""
import os
import sys
import json
import uuid
from datetime import datetime, timedelta

# Adicionar o diretório app ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.utils.database import init_database, get_db_connection
from app.services.memory_service import MemoryService

def generate_uuid():
    """Gerar UUID simples para IDs"""
    return str(uuid.uuid4())

def create_sample_users():
    """Criar usuários padrão"""
    print("Criando usuários padrão...")
    
    users = [
        {
            "id": 1,
            "username": "admin",
            "password_hash": "admin123_hash",
            "email": "admin@iaraflow.com"
        },
        {
            "id": 2,
            "username": "demo_user",
            "password_hash": "demo123_hash",
            "email": "demo@iaraflow.com"
        },
        {
            "id": 3,
            "username": "test_user",
            "password_hash": "test123_hash",
            "email": "test@iaraflow.com"
        }
    ]
    
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            for user in users:
                cur.execute("""
                    INSERT OR REPLACE INTO users (id, username, password_hash, email, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user["id"],
                    user["username"],
                    user["password_hash"],
                    user["email"],
                    datetime.utcnow().isoformat()
                ))
            
            conn.commit()
            print(f"✅ {len(users)} usuários criados com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")

def create_sample_conversations():
    """Criar conversas de exemplo"""
    print("Criando conversas de exemplo...")
    
    memory_service = MemoryService()
    
    conversations = [
        {
            "user_id": "demo_user",
            "session_id": "session_001",
            "messages": [
                {
                    "message": "Olá! Meu nome é João e trabalho como desenvolvedor.",
                    "response": "Olá João! Prazer em conhecê-lo. Como desenvolvedor, você deve ter muita experiência com tecnologia. Em que posso ajudá-lo hoje?"
                },
                {
                    "message": "Lembre-se disso: Tenho 28 anos e moro em São Paulo",
                    "response": "✅ Informação salva na memória! Entendi, João. Você tem 28 anos e mora em São Paulo. Essa informação foi registrada para futuras conversas."
                },
                {
                    "message": "Qual é o meu nome mesmo?",
                    "response": "Seu nome é João! Você me disse isso no início da nossa conversa."
                }
            ]
        },
        {
            "user_id": "test_user",
            "session_id": "session_002",
            "messages": [
                {
                    "message": "Oi, me chamo Maria e sou designer.",
                    "response": "Olá Maria! Que bom conhecê-la. Design é uma área muito criativa e interessante. Como posso ajudá-la hoje?"
                },
                {
                    "message": "Lembre-se disso: Trabalho com UX/UI e adoro café",
                    "response": "✅ Informação salva na memória! Perfeito, Maria! Agora sei que você trabalha com UX/UI e adora café. Essas informações foram salvas para nossas próximas conversas."
                }
            ]
        },
        {
            "user_id": "admin",
            "session_id": "session_003",
            "messages": [
                {
                    "message": "Como administrador, preciso testar o sistema de memória.",
                    "response": "Entendido! Como administrador, você tem acesso completo ao sistema. O sistema de memória está funcionando corretamente e salvando todas as conversas."
                },
                {
                    "message": "Lembre-se disso: Este é um teste do sistema de memória de longo prazo",
                    "response": "✅ Informação salva na memória! Teste registrado com sucesso! O sistema de memória de longo prazo está funcionando perfeitamente."
                }
            ]
        }
    ]
    
    try:
        for conv in conversations:
            user_id = conv["user_id"]
            session_id = conv["session_id"]
            
            for msg_data in conv["messages"]:
                memory_service.save_message_with_profile_update(
                    user_id=user_id,
                    session_id=session_id,
                    message=msg_data["message"],
                    response=msg_data["response"],
                    metadata={
                        "timestamp": datetime.utcnow().isoformat(),
                        "model": "sample_data",
                        "provider": "system",
                        "is_sample": True
                    }
                )
        
        print(f"✅ {len(conversations)} conversas de exemplo criadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar conversas: {e}")

def create_sample_api_keys():
    """Criar chaves de API de exemplo"""
    print("Criando configurações de API de exemplo...")
    
    # Chave Gemini padrão fornecida pelo usuário
    default_gemini_key = "AIzaSyDpLNBaYVrLSzxWj0kLD3v7n75pR5O-AfM"
    
    api_configs = [
        {
            "id": generate_uuid(),
            "user_id": "1",  # admin
            "service": "gemini",
            "api_key": default_gemini_key,
            "is_active": True
        },
        {
            "id": generate_uuid(),
            "user_id": "demo_user",
            "service": "gemini",
            "api_key": default_gemini_key,
            "is_active": True
        },
        {
            "id": generate_uuid(),
            "user_id": "test_user",
            "service": "gemini",
            "api_key": default_gemini_key,
            "is_active": True
        }
    ]
    
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            for config in api_configs:
                cur.execute("""
                    INSERT OR REPLACE INTO api_keys (id, user_id, service, api_key, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    config["id"],
                    config["user_id"],
                    config["service"],
                    config["api_key"],
                    config["is_active"],
                    datetime.utcnow().isoformat()
                ))
            
            conn.commit()
            print(f"✅ {len(api_configs)} configurações de API criadas com sucesso!")
            print(f"   Chave Gemini padrão configurada para todos os usuários: {default_gemini_key[:20]}...")
            
    except Exception as e:
        print(f"❌ Erro ao criar configurações de API: {e}")

def create_sample_app_configs():
    """Criar configurações de aplicativos de exemplo"""
    print("Criando configurações de aplicativos de exemplo...")
    
    app_configs = [
        {
            "id": generate_uuid(),
            "package_name": "com.example.app1",
            "app_name": "App Exemplo 1",
            "stores": json.dumps(["google_play", "app_store"]),
            "collection_frequency": 6,
            "last_collected": (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            "id": generate_uuid(),
            "package_name": "com.example.app2",
            "app_name": "App Exemplo 2",
            "stores": json.dumps(["google_play"]),
            "collection_frequency": 12,
            "last_collected": (datetime.utcnow() - timedelta(hours=5)).isoformat()
        }
    ]
    
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            for config in app_configs:
                cur.execute("""
                    INSERT OR REPLACE INTO app_configs (id, package_name, app_name, stores, collection_frequency, last_collected, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    config["id"],
                    config["package_name"],
                    config["app_name"],
                    config["stores"],
                    config["collection_frequency"],
                    config["last_collected"],
                    datetime.utcnow().isoformat()
                ))
            
            conn.commit()
            print(f"✅ {len(app_configs)} configurações de aplicativos criadas com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao criar configurações de aplicativos: {e}")

def create_sample_reviews():
    """Criar reviews de exemplo"""
    print("Criando reviews de exemplo...")
    
    reviews = [
        {
            "id": generate_uuid(),
            "package_name": "com.example.app1",
            "store": "google_play",
            "review_id": "review_001",
            "user_name": "Usuario1",
            "rating": 5,
            "content": "Aplicativo excelente! Muito fácil de usar e funciona perfeitamente.",
            "review_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "sentiment": "positive",
            "topics": json.dumps(["usabilidade", "funcionalidade"]),
            "keywords": json.dumps(["excelente", "fácil", "perfeito"])
        },
        {
            "id": generate_uuid(),
            "package_name": "com.example.app1",
            "store": "google_play",
            "review_id": "review_002",
            "user_name": "Usuario2",
            "rating": 3,
            "content": "App ok, mas poderia ter mais funcionalidades. Interface é boa.",
            "review_date": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "sentiment": "neutral",
            "topics": json.dumps(["funcionalidades", "interface"]),
            "keywords": json.dumps(["ok", "mais funcionalidades", "boa"])
        },
        {
            "id": generate_uuid(),
            "package_name": "com.example.app2",
            "store": "google_play",
            "review_id": "review_003",
            "user_name": "Usuario3",
            "rating": 2,
            "content": "App trava muito e é lento. Precisa de melhorias urgentes.",
            "review_date": (datetime.utcnow() - timedelta(days=3)).isoformat(),
            "sentiment": "negative",
            "topics": json.dumps(["performance", "bugs"]),
            "keywords": json.dumps(["trava", "lento", "melhorias"])
        }
    ]
    
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            for review in reviews:
                cur.execute("""
                    INSERT OR REPLACE INTO reviews (id, package_name, store, review_id, user_name, rating, content, review_date, sentiment, topics, keywords, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review["id"],
                    review["package_name"],
                    review["store"],
                    review["review_id"],
                    review["user_name"],
                    review["rating"],
                    review["content"],
                    review["review_date"],
                    review["sentiment"],
                    review["topics"],
                    review["keywords"],
                    json.dumps({"is_sample": True}),
                    datetime.utcnow().isoformat()
                ))
            
            conn.commit()
            print(f"✅ {len(reviews)} reviews de exemplo criados com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao criar reviews: {e}")

def main():
    """Função principal para criar todos os dados de exemplo"""
    print("🚀 Iniciando criação de dados padrão para iara-flow-bff...")
    print("=" * 60)
    
    try:
        # Inicializar o banco de dados
        print("Inicializando banco de dados...")
        init_database()
        print("✅ Banco de dados inicializado!")
        print()
        
        # Criar dados de exemplo
        create_sample_users()
        print()
        
        create_sample_conversations()
        print()
        
        create_sample_api_keys()
        print()
        
        create_sample_app_configs()
        print()
        
        create_sample_reviews()
        print()
        
        print("=" * 60)
        print("🎉 Todos os dados padrão foram criados com sucesso!")
        print()
        print("Dados criados:")
        print("- 3 usuários padrão (admin, demo_user, test_user)")
        print("- 3 conversas de exemplo com memória")
        print("- 3 configurações de API")
        print("- 2 configurações de aplicativos")
        print("- 3 reviews de exemplo")
        print()
        print("O sistema está pronto para uso!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

