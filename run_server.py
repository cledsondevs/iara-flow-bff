import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente primeiro
load_dotenv()

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )


