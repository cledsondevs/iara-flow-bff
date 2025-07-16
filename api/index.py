import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

# O Vercel espera que a aplicação Flask seja exportada diretamente como 'app'
# Não é necessário uma função handler para request/response

# Para compatibilidade com Vercel (se rodar localmente com `python api/index.py`)
if __name__ == "__main__":
    app.run()


