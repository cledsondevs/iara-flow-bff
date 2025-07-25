from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from app.chats.services.gemini_chat_service import GeminiChatService
from app.chats.services.openai_chat_service import OpenAIChatService
# from app.chats.services.groq_chat_service import GroqChatService # Removido

chat_bp = Blueprint("chat", __name__)

# Inicializar serviços
gemini_service = GeminiChatService()
openai_service = OpenAIChatService()
# groq_service = GroqChatService() # Removido

@chat_bp.route("/gemini/chat", methods=["POST"])
@cross_origin()
def gemini_chat():
    """Endpoint para conversar com o Gemini com memória de longo prazo"""
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
        
        # Processar mensagem com o Gemini
        response = gemini_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "timestamp": response["timestamp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem com Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/chat", methods=["POST"])
@cross_origin()
def openai_chat():
    """Endpoint para conversar com o OpenAI com memória de longo prazo"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_message = data.get("message")
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        model = data.get("model")  # Opcional: permite especificar o modelo
        
        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        # Processar mensagem com o OpenAI
        response = openai_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id,
            model=model
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "usage": response["usage"],
            "timestamp": response["timestamp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem com OpenAI: {str(e)}"}), 500


@chat_bp.route("/gemini/memory", methods=["GET"])
@cross_origin()
def get_gemini_memory():
    """Recuperar memória do chat Gemini para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = gemini_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória do Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/memory", methods=["GET"])
@cross_origin()
def get_openai_memory():
    """Recuperar memória do chat OpenAI para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = openai_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória do OpenAI: {str(e)}"}), 500


@chat_bp.route("/gemini/memory", methods=["DELETE"])
@cross_origin()
def clear_gemini_memory():
    """Limpar memória do chat Gemini para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        gemini_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória do Gemini limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória do Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/memory", methods=["DELETE"])
@cross_origin()
def clear_openai_memory():
    """Limpar memória do chat OpenAI para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        openai_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória do OpenAI limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória do OpenAI: {str(e)}"}), 500


@chat_bp.route("/chat/health", methods=["GET"])
@cross_origin()
def health_check():
    """Endpoint de verificação de saúde dos chats"""
    return jsonify({
        "success": True,
        "message": "Serviços de chat Gemini e OpenAI estão funcionando!",
        "services": ["gemini", "openai"],
        "timestamp": datetime.utcnow().isoformat()
    }), 200


