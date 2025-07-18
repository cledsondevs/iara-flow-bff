import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

if __name__ == '__main__':
    app.run()
