import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config.settings import config
from app.utils.database import init_database
from app.auth.auth_routes import auth_bp
from app.api.routes.agent_routes import agent_bp
from app.api.routes.gemini_agent_routes import gemini_agent_bp
from app.api.routes.openai_agent_routes import openai_agent_bp
from app.api.routes.review_agent_routes import review_agent_bp
from app.api.routes.data_analysis_routes import data_analysis_bp
from app.api.routes.dashboard_routes import dashboard_bp
from app.chats.routes.chat_routes import chat_bp
from app.api.routes.api_key_routes import api_key_bp

def create_app(config_name='default'):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Carregar configurações
    app.config.from_object(config[config_name])
    
    # Configurar CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])
    
    # Inicializar banco de dados
    try:
        init_database()
        print("Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
    
    # Inicializar MemoryService para garantir que as tabelas sejam criadas
    try:
        from app.services.memory_service import MemoryService
        memory_service = MemoryService()
        print("MemoryService inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar MemoryService: {e}")
    
    # Criar usuário padrão se não existir
    try:
        from app.auth.auth_routes import get_db_connection
        import bcrypt
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar se já existe um usuário admin
        cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        existing_user = cur.fetchone()
        
        if not existing_user:
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
            conn.commit()
            print(f"Usuário padrão criado: {username}/{password}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao criar usuário padrão: {e}")
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(agent_bp, url_prefix="/api")
    app.register_blueprint(gemini_agent_bp, url_prefix="/api")
    app.register_blueprint(openai_agent_bp, url_prefix="/api/openai")
    app.register_blueprint(review_agent_bp)
    app.register_blueprint(data_analysis_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(api_key_bp, url_prefix="/api")

    @app.route("/")
    def health_check():
        """Endpoint de health check"""
        return {"status": "ok", "message": "Iara Flow BFF is running"}
    
    @app.route("/<path:path>")
    def serve(path):
        """Servir arquivos estáticos"""
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    return app

def main():
    """Função principal para executar a aplicação"""
    config_name = os.getenv("FLASK_ENV", "default")
    app = create_app(config_name)
    
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )

if __name__ == "__main__":
    main()

