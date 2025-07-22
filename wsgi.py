import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

# Importar a função create_app do seu módulo principal
from app.main import create_app

# Criar a instância da aplicação Flask
application = create_app()

