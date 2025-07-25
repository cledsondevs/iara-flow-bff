"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações base da aplicação"""
    SECRET_KEY = os.getenv("SECRET_KEY", "asdf#FGSgvasgf")
    DATABASE_PATH = os.getenv("DB_PATH", os.path.abspath("./data/iara_flow.db"))
    
    # Configurações do OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Configurações do Google Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBCDajU2VLuNYuKrFTBz452x5dpulmLfG0")
    
    # Configurações de CORS
    CORS_ORIGINS = "*"
    
    # Configurações de sessão
    SESSION_TIMEOUT_HOURS = 24
    
    # Configurações de debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configurações do servidor
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 5000))

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False

# Configuração padrão
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


