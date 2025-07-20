
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import uuid
from datetime import datetime
from src.services.dynamodb_service import DynamoDBService
from src.services.flow_executor import FlowExecutor

flow_dynamodb_bp = Blueprint("flow_dynamodb", __name__)
dynamodb_service = DynamoDBService()
flow_executor = FlowExecutor()

@flow_dynamodb_bp.route("/flows", methods=["POST"])
@cross_origin()
def create_flow():
    """Criar um novo fluxo"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        flow_data = data.get("flow_data", {})
        
        # Validar fluxo
        validation = flow_executor.validate_flow(flow_data)
        if not validation["valid"]:
            return jsonify({
                "error": "Fluxo inválido",
                "validation_errors": validation["errors"]
            }), 400
        
        # Criar fluxo no DynamoDB
        result = dynamodb_service.create_flow(data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "flow": result["flow"],
                "validation_warnings": validation.get("warnings", [])
            }), 201
        else:
            return jsonify({"error": result["error"]}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao criar fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows", methods=["GET"])
@cross_origin()
def list_flows():
    """Listar todos os fluxos"""
    try:
        result = dynamodb_service.list_flows()
        
        if result["success"]:
            return jsonify({
                "success": True,
                "flows": result["flows"]
            })
        else:
            return jsonify({"error": result["error"]}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar fluxos: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>", methods=["GET"])
@cross_origin()
def get_flow(flow_id):
    """Obter um fluxo específico"""
    try:
        result = dynamodb_service.get_flow(flow_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "flow": result["flow"]
            })
        else:
            return jsonify({"error": result["error"]}), 404 if "não encontrado" in result["error"] else 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>", methods=["PUT"])
@cross_origin()
def update_flow(flow_id):
    """Atualizar um fluxo"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Validar novo fluxo se flow_data foi fornecido
        if "flow_data" in data:
            validation = flow_executor.validate_flow(data["flow_data"])
            if not validation["valid"]:
                return jsonify({
                    "error": "Fluxo inválido",
                    "validation_errors": validation["errors"]
                }), 400
        
        # Atualizar fluxo no DynamoDB
        result = dynamodb_service.update_flow(flow_id, data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "flow": result["flow"]
            })
        else:
            return jsonify({"error": result["error"]}), 404 if "não encontrado" in result["error"] else 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>", methods=["DELETE"])
@cross_origin()
def delete_flow(flow_id):
    """Deletar um fluxo"""
    try:
        result = dynamodb_service.delete_flow(flow_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": result["message"]
            })
        else:
            return jsonify({"error": result["error"]}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>/execute", methods=["POST"])
@cross_origin()
def execute_flow(flow_id):
    """Executar um fluxo"""
    try:
        # Obter fluxo do DynamoDB
        flow_result = dynamodb_service.get_flow(flow_id)
        if not flow_result["success"]:
            return jsonify({"error": flow_result["error"]}), 404
        
        flow = flow_result["flow"]
        
        data = request.get_json() or {}
        input_data = data.get("input", "")
        
        # Criar execução no DynamoDB
        execution_data = {
            "flow_id": flow_id,
            "input_data": {"user_input": input_data},
            "status": "running"
        }
        
        execution_result = dynamodb_service.create_execution(execution_data)
        if not execution_result["success"]:
            return jsonify({"error": execution_result["error"]}), 500
        
        execution = execution_result["execution"]
        execution_id = execution["id"]
        
        try:
            # Executar fluxo
            flow_data = flow["flow_data"]
            result = flow_executor.execute_flow(flow_data, input_data)
            
            # Atualizar execução com resultado
            update_data = {
                "completed_at": datetime.utcnow().isoformat()
            }
            
            if result["success"]:
                update_data.update({
                    "status": "completed",
                    "output_data": {
                        "output": result["output"],
                        "execution_path": result["execution_path"],
                        "node_outputs": result["node_outputs"]
                    }
                })
            else:
                update_data.update({
                    "status": "failed",
                    "error_message": result["error"]
                })
            
            # Atualizar execução
            update_result = dynamodb_service.update_execution(execution_id, update_data)
            if not update_result["success"]:
                print(f"Erro ao atualizar execução: {update_result['error']}")
            
            # Atualizar status do fluxo
            flow_update_data = {
                "status": update_data["status"]
            }
            flow_update_result = dynamodb_service.update_flow(flow_id, flow_update_data)
            if not flow_update_result["success"]:
                print(f"Erro ao atualizar fluxo: {flow_update_result['error']}")
            
            # Obter execução atualizada
            final_execution_result = dynamodb_service.get_execution(execution_id)
            final_execution = final_execution_result["execution"] if final_execution_result["success"] else execution
            
            return jsonify({
                "success": update_data["status"] == "completed",
                "execution": final_execution,
                "output": final_execution["output_data"].get("output") if update_data["status"] == "completed" else None,
                "error": update_data.get("error_message") if update_data["status"] == "failed" else None
            })
            
        except Exception as e:
            # Atualizar execução com erro
            error_update_data = {
                "status": "failed",
                "error_message": str(e),
                "completed_at": datetime.utcnow().isoformat()
            }
            
            dynamodb_service.update_execution(execution_id, error_update_data)
            
            return jsonify({
                "success": False,
                "execution": execution,
                "error": str(e)
            })
        
    except Exception as e:
        return jsonify({"error": f"Erro ao executar fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>/validate", methods=["POST"])
@cross_origin()
def validate_flow(flow_id):
    """Validar um fluxo"""
    try:
        # Obter fluxo do DynamoDB
        flow_result = dynamodb_service.get_flow(flow_id)
        if not flow_result["success"]:
            return jsonify({"error": flow_result["error"]}), 404
        
        flow = flow_result["flow"]
        flow_data = flow["flow_data"]
        validation = flow_executor.validate_flow(flow_data)
        
        return jsonify({
            "success": True,
            "validation": validation
        })
        
    except Exception as e:
        return jsonify({"error": f"Erro ao validar fluxo: {str(e)}"}), 500

@flow_dynamodb_bp.route("/flows/<flow_id>/executions", methods=["GET"])
@cross_origin()
def get_flow_executions(flow_id):
    """Obter execuções de um fluxo"""
    try:
        result = dynamodb_service.get_flow_executions(flow_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "executions": result["executions"]
            })
        else:
            return jsonify({"error": result["error"]}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter execuções: {str(e)}"}), 500

@flow_dynamodb_bp.route("/executions/<execution_id>", methods=["GET"])
@cross_origin()
def get_execution(execution_id):
    """Obter uma execução específica"""
    try:
        result = dynamodb_service.get_execution(execution_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "execution": result["execution"]
            })
        else:
            return jsonify({"error": result["error"]}), 404 if "não encontrada" in result["error"] else 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter execução: {str(e)}"}), 500

