from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from src.services.langchain_agent_service import LangChainAgentService

agent_bp = Blueprint("agent", __name__)
agent_service = LangChainAgentService()

@agent_bp.route("/agent/chat", methods=["POST"])
@cross_origin()
def chat_with_agent():
    """Endpoint principal para conversar com o agente de IA"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_message = data.get("message")
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        # Invocar o agente LangChain
        response = agent_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem: {str(e)}"}), 500

@agent_bp.route("/agent/memory", methods=["GET"])
@cross_origin()
def get_agent_memory():
    """Recuperar memória do agente para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = agent_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória: {str(e)}"}), 500

@agent_bp.route("/agent/memory", methods=["DELETE"])
@cross_origin()
def clear_agent_memory():
    """Limpar memória do agente para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        agent_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória: {str(e)}"}), 500

@agent_bp.route("/agent/health", methods=["GET"])
@cross_origin()
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        "success": True,
        "message": "Agente de IA está funcionando!",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

