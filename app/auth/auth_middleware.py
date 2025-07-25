from functools import wraps
from flask import request, jsonify
import sqlite3
import os

DATABASE_PATH = os.getenv('DB_PATH', './data/iara_flow.db')

def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn

def require_auth(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar token de sessão no header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token de autorização necessário'}), 401
        
        session_token = auth_header.split(' ')[1]
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Verificar se a sessão é válida
            cur.execute(
                """
                SELECT s.user_id, u.username, u.email 
                FROM sessions s 
                JOIN users u ON s.user_id = u.id 
                WHERE s.session_token = ? AND s.expires_at > datetime('now')
                """,
                (session_token,)
            )
            session_data = cur.fetchone()
            
            cur.close()
            conn.close()
            
            if not session_data:
                return jsonify({'error': 'Sessão inválida ou expirada'}), 401
            
            # Adicionar informações do usuário ao request
            request.current_user = {
                'id': session_data[0],
                'username': session_data[1],
                'email': session_data[2]
            }
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return decorated_function

def get_current_user():
    """Função helper para obter o usuário atual da requisição"""
    return getattr(request, 'current_user', None)

