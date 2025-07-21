"""
Utilitários para banco de dados SQLite
"""
import sqlite3
import os
from app.config.settings import Config

def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite"""
    # Garantir que o diretório do banco existe
    db_path = Config.DATABASE_PATH
    db_dir = os.path.dirname(db_path)
    
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"Diretório criado: {db_dir}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn

def init_database():
    """Inicializar todas as tabelas do banco de dados"""
    try:
        conn = get_db_connection()
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
        
        # Tabela de memórias (para o agente)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
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
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("Banco de dados inicializado com sucesso")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        raise

