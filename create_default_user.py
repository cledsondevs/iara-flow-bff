#!/usr/bin/env python3
"""
Script para criar usuário padrão no banco de dados
"""
import os
import sys
import sqlite3
import bcrypt
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from app.config.settings import Config
from app.utils.database import init_database

def create_default_user():
    """Criar usuário padrão no banco de dados"""
    try:
        # Inicializar banco de dados primeiro
        print("Inicializando banco de dados...")
        init_database()
        
        # Garantir que o diretório do banco existe
        db_path = Config.DATABASE_PATH
        db_dir = os.path.dirname(db_path)
        
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Diretório criado: {db_dir}")
        
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Verificar se já existe um usuário admin
        cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        existing_user = cur.fetchone()
        
        if existing_user:
            print("Usuário admin já existe no banco de dados")
            return
        
        # Criar usuário padrão
        username = "admin"
        password = "admin"
        email = "admin@iaraflow.com"
        
        # Hash da senha
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Inserir usuário
        cur.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        user_id = cur.lastrowid
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Usuário padrão criado com sucesso!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print(f"User ID: {user_id}")
        
    except Exception as e:
        print(f"Erro ao criar usuário padrão: {e}")
        raise

if __name__ == "__main__":
    create_default_user()

