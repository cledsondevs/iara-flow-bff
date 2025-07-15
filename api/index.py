import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

# Exportar a aplicação para o Vercel
def handler(request, response):
    return app(request, response)

# Para compatibilidade com Vercel
if __name__ == "__main__":
    app.run()

