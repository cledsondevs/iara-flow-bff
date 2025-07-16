from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import uuid
from datetime import datetime
from src.services.flow_executor import FlowExecutor
from src.services.langchain_agent import invoke_langchain_agent

flow_execution_bp = Blueprint("flow_execution", __name__)
flow_executor = FlowExecutor()

@flow_execution_bp.route("/execute", methods=["POST"])
@cross_origin()
def execute_flow_direct():
    """Executar um fluxo diretamente a partir do JSON"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        flow_data = data.get("flow_data")
        input_data = data.get("input", "")
        user_id = data.get("user_id") # Obter user_id da requisição
        
        if not flow_data:
            return jsonify({"error": "flow_data é obrigatório"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400

        # Aqui, em vez de executar o flow_executor, vamos invocar o agente LangChain
        # O flow_data pode ser usado para configurar o agente (quais ferramentas ele tem acesso, etc.)
        # Por enquanto, vamos passar o input_data diretamente para o agente
        result_agent = invoke_langchain_agent(input_data, user_id)
        
        return jsonify({
            "success": True,
            "output": result_agent,
            "message": "Agente LangChain invocado com sucesso."
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao executar fluxo: {str(e)}"}), 500

@flow_execution_bp.route("/validate", methods=["POST"])
@cross_origin()
def validate_flow_direct():
    """Validar um fluxo diretamente a partir do JSON"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        flow_data = data.get("flow_data")
        
        if not flow_data:
            return jsonify({"error": "flow_data é obrigatório"}), 400
        
        # Validar fluxo
        validation = flow_executor.validate_flow(flow_data)
        
        return jsonify({
            "success": True,
            "validation": validation
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao validar fluxo: {str(e)}"}), 500

@flow_execution_bp.route("/test", methods=["GET"])
@cross_origin()
def test_endpoint():
    """Endpoint de teste para verificar se a API está funcionando"""
    return jsonify({
        "success": True,
        "message": "API de execução de fluxos está funcionando!",
        "timestamp": datetime.utcnow().isoformat()
    }), 200
