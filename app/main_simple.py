import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Definir variáveis de ambiente para as chaves da API de receita
os.environ["RECIPE_API_KEY"] = os.getenv("RECIPE_API_KEY", "YOUR_RECIPE_API_KEY")
os.environ["RECIPE_APP_ID"] = os.getenv("RECIPE_APP_ID", "YOUR_RECIPE_APP_ID")

# DON\'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.flow_execution import flow_execution_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), \'static\'))
app.config[\'SECRET_KEY\'] = \'asdf#FGSgvasgf$5$WGT\'

# Configurar CORS
CORS(app, origins="*")

# Registrar apenas o blueprint de execução (sem DynamoDB)
app.register_blueprint(flow_execution_bp, url_prefix=\'/api/flow\')

@app.route(\'/\', defaults={\'path\': \'\'}) 
@app.route(\'/<path:path>\')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, \'index.html\')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, \'index.html\')
        else:
            return "index.html not found", 404

@app.route(\'/health\')
def health():
    return {"status": "ok", "message": "API funcionando"}

if __name__ == \'__main__\':
    app.run(host=\'0.0.0.0\', port=5000, debug=True)


