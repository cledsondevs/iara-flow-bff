from flask import Blueprint, request, jsonify, session
import psycopg2
import bcrypt
import secrets
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost:5432/admin')

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL"""
    return psycopg2.connect(DATABASE_URL)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Endpoint para registro de novos usuários"""
    try:
        data = request.get_json()
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
                "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s) RETURNING id",
                (username, password_hash, email)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            
            return jsonify({
                'message': 'Usuário criado com sucesso',
                'user_id': user_id
            }), 201
            
        except psycopg2.IntegrityError:
            return jsonify({'error': 'Username ou email já existe'}), 409
        finally:
            cur.close()
            conn.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint para login de usuários"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Buscar usuário
        cur.execute(
            "SELECT id, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        user_id = user[0]
        
        # Gerar token de sessão
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)  # Sessão válida por 24 horas
        
        # Salvar sessão no banco
        cur.execute(
            "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (%s, %s, %s)",
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

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Endpoint para logout de usuários"""
    try:
        data = request.get_json()
        session_token = data.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Token de sessão é obrigatório'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Remover sessão do banco
        cur.execute(
            "DELETE FROM sessions WHERE session_token = %s",
            (session_token,)
        )
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/verify', methods=['POST'])
def verify_session():
    """Endpoint para verificar se uma sessão é válida"""
    try:
        data = request.get_json()
        session_token = data.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Token de sessão é obrigatório'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar sessão
        cur.execute(
            """
            SELECT s.user_id, s.expires_at, u.username, u.email 
            FROM sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = %s AND s.expires_at > NOW()
            """,
            (session_token,)
        )
        session_data = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not session_data:
            return jsonify({'error': 'Sessão inválida ou expirada'}), 401
        
        return jsonify({
            'valid': True,
            'user_id': session_data[0],
            'username': session_data[2],
            'email': session_data[3],
            'expires_at': session_data[1].isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint para obter informações do usuário"""
    try:
        # Verificar token de sessão no header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token de autorização necessário'}), 401
        
        session_token = auth_header.split(' ')[1]
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar se a sessão é válida e pertence ao usuário
        cur.execute(
            """
            SELECT s.user_id FROM sessions s 
            WHERE s.session_token = %s AND s.expires_at > NOW() AND s.user_id = %s
            """,
            (session_token, user_id)
        )
        
        if not cur.fetchone():
            return jsonify({'error': 'Acesso não autorizado'}), 403
        
        # Buscar informações do usuário
        cur.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'created_at': user[3].isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500