from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from app.services.gemini_agent_service import GeminiAgentService

gemini_agent_bp = Blueprint("gemini_agent", __name__)

@gemini_agent_bp.route("/gemini/chat", methods=["POST"])
@cross_origin()
def chat_with_gemini_agent():
    """Endpoint para conversar com o agente Gemini"""
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
        
        # Criar instância do serviço Gemini
        gemini_service = GeminiAgentService()
        
        # Processar mensagem
        response = gemini_service.process_message(
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

@gemini_agent_bp.route("/gemini/memory", methods=["GET"])
@cross_origin()
def get_gemini_agent_memory():
    """Recuperar memória do agente Gemini para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        gemini_service = GeminiAgentService()
        memory = gemini_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória: {str(e)}"}), 500

@gemini_agent_bp.route("/gemini/memory", methods=["DELETE"])
@cross_origin()
def clear_gemini_agent_memory():
    """Limpar memória do agente Gemini para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        gemini_service = GeminiAgentService()
        gemini_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória: {str(e)}"}), 500

@gemini_agent_bp.route("/gemini/health", methods=["GET"])
@cross_origin()
def gemini_health_check():
    """Endpoint de verificação de saúde da API Gemini"""
    return jsonify({
        "success": True,
        "message": "Agente Gemini está funcionando!",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

