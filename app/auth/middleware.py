"""
Middleware de autenticação
"""
from functools import wraps
from flask import request, jsonify
from app.utils.database import get_db_connection

def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
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
                SELECT s.user_id, u.username FROM sessions s 
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
                'user_id': session_data[0],
                'username': session_data[1]
            }
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Erro na verificação de autenticação'}), 500
    
    return decorated_function

def get_current_user():
    """Obter o usuário atual da requisição"""
    return getattr(request, 'current_user', None)

