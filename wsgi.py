import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

# Importar o app Flask
from src.main import app

# Variável que o Gunicorn precisa encontrar
application = app
