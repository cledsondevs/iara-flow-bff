from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import uuid
from datetime import datetime
from src.services.flow_executor import FlowExecutor

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
        
        if not flow_data:
            return jsonify({"error": "flow_data é obrigatório"}), 400
        
        # Validar fluxo
        validation = flow_executor.validate_flow(flow_data)
        if not validation["valid"]:
            return jsonify({
                "error": "Fluxo inválido",
                "validation_errors": validation["errors"]
            }), 400
        
        # Executar fluxo
        result = flow_executor.execute_flow(flow_data, input_data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "output": result["output"],
                "execution_path": result["execution_path"],
                "node_outputs": result["node_outputs"],
                "validation_warnings": validation.get("warnings", [])
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
        
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

