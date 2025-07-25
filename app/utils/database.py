"""
Utilitários para banco de dados SQLite
"""
import sqlite3
import os
from app.config.settings import Config

from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite usando um context manager"""
    # Garantir que o diretório do banco existe
    db_path = Config.DATABASE_PATH
    db_dir = os.path.dirname(db_path)
    
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"Diretório criado: {db_dir}")
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def init_database():
    """Inicializar todas as tabelas do banco de dados"""
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Tabela de usuários
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de sessões
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Tabela de conversas (para o agente)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Tabela para perfil/memória global do usuário
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL UNIQUE,
                    profile_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de flows
            cur.execute("""
                CREATE TABLE IF NOT EXISTS flows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    config TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            # Tabela para chaves de API
            cur.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    service TEXT NOT NULL,
                    api_key TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, service)
                )
            """)
            
            # Tabela de reviews
            cur.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id TEXT PRIMARY KEY,
                    package_name TEXT NOT NULL,
                    store TEXT NOT NULL,
                    review_id TEXT UNIQUE NOT NULL,
                    user_name TEXT,
                    rating INTEGER,
                    content TEXT,
                    review_date TEXT,
                    sentiment TEXT,
                    topics TEXT,
                    keywords TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de configurações de aplicativos
            cur.execute("""
                CREATE TABLE IF NOT EXISTS app_configs (
                    id TEXT PRIMARY KEY,
                    package_name TEXT UNIQUE NOT NULL,
                    app_name TEXT NOT NULL,
                    stores TEXT,
                    collection_frequency INTEGER,
                    last_collected TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de padrões de sentimento
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    sentiment_trend TEXT,
                    keywords TEXT,
                    frequency INTEGER,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(package_name, topic)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backlog_items (
                    id TEXT PRIMARY KEY,
                    package_name TEXT NOT NULL,
                    review_id TEXT,
                    category TEXT,
                    priority INTEGER,
                    description TEXT,
                    status TEXT,
                    assigned_to TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de otimizações de backlog
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backlog_optimizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    success_indicators TEXT,
                    failure_indicators TEXT,
                    optimization_rules TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de evolução de sentimento
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_evolution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    sentiment_distribution TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            
            print("Banco de dados inicializado com sucesso")
            
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        raise
