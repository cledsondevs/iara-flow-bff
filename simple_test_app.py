#!/usr/bin/env python3
"""
Aplicação simplificada para testar as rotas de autenticação
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import secrets
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
CORS(app, origins="*")

DATABASE_PATH = './iara_flow.db'

def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializar tabelas do banco de dados"""
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
        
        conn.commit()
        cur.close()
        conn.close()
        print("Banco de dados inicializado com sucesso")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")

@app.route('/')
def health_check():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'message': 'Iara Flow BFF is running'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Endpoint para registro de novos usuários"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        # Hash da senha
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Inserir novo usuário
            cur.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            user_id = cur.lastrowid
            conn.commit()
            
            return jsonify({
                'message': 'Usuário criado com sucesso',
                'user_id': user_id
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username ou email já existe'}), 409
        finally:
            cur.close()
            conn.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint para login de usuários"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Buscar usuário
        cur.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cur.fetchone()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            cur.close()
            conn.close()
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        user_id = user[0]
        
        # Gerar token de sessão
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        # Salvar sessão no banco
        cur.execute(
            "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)",
            (user_id, session_token, expires_at)
        )
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'session_token': session_token,
            'user_id': user_id,
            'expires_at': expires_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5001, debug=False)

