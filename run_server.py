import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente primeiro
load_dotenv()

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

# Criar uma aplicação Flask simples para testar
app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/agent/health', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "success": True,
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
